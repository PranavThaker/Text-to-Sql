import json
import time
from collections import Counter, defaultdict

from pipeline.graph import app
from pipeline.executor import execute_query


def compare_results(generated_result, reference_result):
    if not generated_result.get("success"):
        return False

    if not reference_result.get("success"):
        return False

    return (
        Counter(tuple(row) for row in generated_result["rows"])
        ==
        Counter(tuple(row) for row in reference_result["rows"])
    )


def compute_accuracy(results):
    total = len(results)

    if total == 0:
        return {
            "overall": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "accuracy": 0.0
            },
            "by_difficulty": {}
        }

    passed = sum(
        1 for result in results
        if result["passed"]
    )

    failed = total - passed

    overall_accuracy = (passed / total) * 100

    difficulty_stats = defaultdict(lambda: {
        "total": 0,
        "passed": 0,
        "failed": 0
    })

    for result in results:
        difficulty = result.get("difficulty", "unknown")

        difficulty_stats[difficulty]["total"] += 1

        if result["passed"]:
            difficulty_stats[difficulty]["passed"] += 1
        else:
            difficulty_stats[difficulty]["failed"] += 1

    for difficulty, stats in difficulty_stats.items():
        stats["accuracy"] = (
            stats["passed"] / stats["total"]
        ) * 100

    return {
        "overall": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "accuracy": overall_accuracy
        },
        "by_difficulty": dict(difficulty_stats)
    }


def run_benchmark():

    with open("evaluation/benchmark.json", "r") as file:
        data = json.load(file)

    benchmark_results = []
    total_tests = len(data)

    for i, obj in enumerate(data, start=1):

        question = obj["question"]
        reference_sql = obj["sql"]
        difficulty = obj.get("difficulty", "unknown")

        print(f"\n{'=' * 60}")
        print(f"Running test {i}/{total_tests}")
        print(f"Difficulty: {difficulty}")
        print(f"Question: {question}")
        print(f"{'=' * 60}")

        initial_state = {
            "question": question,
            "retrieved_context": {},
            "generated_sql": "",
            "execution_result": {},
            "retry_count": 0,
            "last_error": ""
        }

        try:
            # Run Text-to-SQL pipeline
            result = app.invoke(initial_state)

            generated_sql = result.get("generated_sql", "")
            generated_result = result.get("execution_result", {})

            # Execute reference SQL
            reference_result = execute_query(reference_sql)

            # Compare generated result with reference result
            comparison_result = compare_results(
                generated_result,
                reference_result
            )

            if comparison_result:

                print("Result: PASS")

                benchmark_results.append({
                    "test_number": i,
                    "question": question,
                    "difficulty": difficulty,
                    "passed": True
                })

            else:

                print("Result: FAIL")

                benchmark_results.append({
                    "test_number": i,
                    "question": question,
                    "difficulty": difficulty,
                    "passed": False,

                    "generated_sql": generated_sql,
                    "reference_sql": reference_sql,

                    "generated_result": generated_result,
                    "reference_result": reference_result,

                    "retry_count": result.get("retry_count", 0),
                    "last_error": result.get("last_error", "")
                })

        except Exception as e:

            error_message = str(e)

            print(f"ERROR: {error_message}")

            benchmark_results.append({
                "test_number": i,
                "question": question,
                "difficulty": difficulty,
                "passed": False,

                "generated_sql": "",
                "reference_sql": reference_sql,

                "generated_result": {},
                "reference_result": {},

                "retry_count": initial_state["retry_count"],
                "last_error": error_message,

                "exception": type(e).__name__
            })

        finally:

            print(f"Test {i}/{total_tests} completed.")

            # Cooldown after every 3 tests
            if i % 8 == 0 and i < total_tests:

                print("3 tests completed.")
                print("Sleeping for 60 seconds before the next test...")

                time.sleep(60)

    # Compute accuracy
    accuracy = compute_accuracy(benchmark_results)

    # Save results
    output = {
        "results": benchmark_results,
        "accuracy": accuracy
    }

    with open("evaluation/results.json", "w") as file:
        json.dump(output, file, indent=4,default=str)

    # Print summary
    print("\nOverall Results")
    print("----------------")
    print(f"Total:    {accuracy['overall']['total']}")
    print(f"Passed:   {accuracy['overall']['passed']}")
    print(f"Failed:   {accuracy['overall']['failed']}")
    print(f"Accuracy: {accuracy['overall']['accuracy']:.2f}%")

    print("\nBy Difficulty")
    print("----------------")

    for difficulty, stats in accuracy["by_difficulty"].items():

        print(
            f"{difficulty}: "
            f"{stats['passed']}/{stats['total']} passed "
            f"({stats['accuracy']:.2f}%)"
        )

    return accuracy


if __name__ == "__main__":
    run_benchmark()