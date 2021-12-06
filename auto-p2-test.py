import subprocess
import pytest
import os
from jsonschema import validate


def test_fails_if_no_order_provided():
    try:
        subprocess.check_output(["auto-p2.py"])
        assert False, "KO - Launching program with no arguments should fail"
    except:
        assert True, "OK - Program launch has failed as expected"


@pytest.mark.parametrize("wrong_order", [
    "prepre",
    "stap",
    "lunch"
])
def test_fails_if_wrong_order_provided(wrong_order):
    try:
        subprocess.check_output(["auto-p2.py", wrong_order])
        assert False, "KO - Launching program with wrong arguments should fail"
    except:
        assert True, "OK - Program launch has failed as expected"


@pytest.mark.parametrize("correct_order", [
    "stop",
    "launch",
    "release",
    "prepare"
])
def test_success_if_correct_and_single_order_provided(correct_order):
    try:
        subprocess.check_output(["auto-p2.py", correct_order])
        assert True, "OK - Launching program with correct argument should success"
    except:
        assert False, "KO - Program launch should not have failed as their arguments were correct"


@pytest.mark.parametrize("not_combinable_order", [
    "stop",
    "launch",
    "release"
])
def test_fails_if_wrong_combination_of_order_and_num_serv(not_combinable_order):
    try:
        subprocess.check_output(["auto-p2.py", not_combinable_order, "-n", "2"])
        assert False, f"KO - Combining {not_combinable_order} with num_serv should fail"
    except:
        assert True, "OK - Program launch has failed as expected"


@pytest.mark.parametrize("num_serv", [
    "1", "2", "3", "4", "5"
])
def test_success_if_correct_combination_of_order_and_num_serv(num_serv):
    try:
        subprocess.check_output(["auto-p2.py", "prepare", "-n", num_serv])
        assert True, f"OK - Combining prepare with num_serv should succeed"
    except:
        assert False, "KO - Program launch should not have failed as their arguments were correct"


@pytest.mark.parametrize("num_serv", [
    "0", "-1", "300", "1000", "0.1"
])
def test_fail_if_wrong_num_serv_is_provided(num_serv):
    try:
        subprocess.check_output(["auto-p2.py", "prepare", "-n", num_serv])
        assert False, f"KO - Wrong num_serv should make the script fail"
    except:
        assert True, "OK - Program launch has failed as expected"


# TODO
""" def test_no_num_serv_provided_fallbacks_to_default():
    try:
        subprocess.check_output(f"auto-p2.py prepare", shell=True)
        assert True, f"OK - Combining prepare with num_serv should succeed"
    except:
        assert False, "KO - Program launch should not have failed as their arguments were correct" """


def test_prepare_command_create_config_file():
    subprocess.check_output(["auto-p2.py", "prepare"])
    assert os.path.exists(
        'auto-p2.json'), "KO - The expected file created with prepare command is not present"

@pytest.mark.parametrize("num_serv", [
    "1", "2", "3", "4", "5"
])
def test_prepare_command_create_json_with_expect_schema(num_serv):
    subprocess.check_output(["auto-p2.py", "prepare", "-n", num_serv])
    schema = {
        "num_serv": {"type": "number"}
    }
    try:
        validate(instance=open('auto-p2.json').read(), schema=schema)
        assert True, f"OK - The configuration file content matches the schema expected"
    except:
        assert False, f"KO - The configuration file content doesn't match the schema expected"


@pytest.mark.parametrize("num_serv", [
    "1", "2", "3", "4", "5"
])
def test_prepare_command_fills_correctly_config_file(num_serv):
    subprocess.check_output(["auto-p2.py", "prepare", "-n", num_serv])
    assert str(num_serv) in open('auto-p2.json').read(),  f"KO - The configuration file content does contain the expected number of servers"
