import json
import tempfile

import pytest

from drunc_fsm_actions.utils import setenv

dotdrunc_json = {
    "run_registry_configuration": {
        "socket": "http://bananas:1234",
        "user": "jcvandamme",
        "password": "karate",
    },
    "run_number_configuration": {
        "socket": "http://bananas:1234",
        "user": "jcvandamme",
        "password": "karate",
    },
    "elisa_configuration": {
        "some-detector": {
            "socket": "http://bananas:1234",
            "user": "jcvandamme",
            "password": "karate",
        },
    },
}


class MockOKSKey:
    session = "local-1x1-config"


class MockDetectorConfiguration:
    id = "dummy-detector"


class MockDAL:
    detector_configuration = MockDetectorConfiguration()


class MockDB:
    def get_dal(self, class_name, uid):
        return MockDAL()


class MockConfiguration:
    oks_key = MockOKSKey()
    initial_data = "oksconflibs:config/daqsystemtest/example-configs.data.xml"
    db = MockDB()


class MockActor:
    def get_user_name(self) -> str:
        return "jcvandamme"


class MockController:
    configuration = MockConfiguration()
    actor = MockActor()
    session = "local-1x1-config"
    name = "root-controller"
    opmon_publisher = None


class MockFileNameParameter:
    def __init__(self, name="file_name") -> None:
        self.name = name
        self.value = tempfile.NamedTemporaryFile(delete=True).name


class MockParameter:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value


class MockConfiguration:
    def __init__(self, parameters=None, file_parameters=None) -> None:
        if file_parameters is None:
            file_parameters = []
        if parameters is None:
            parameters = {}
        self.parameters = [
            MockParameter(name, value) for name, value in parameters.items()
        ]
        self.parameters += [MockFileNameParameter(name) for name in file_parameters]


@pytest.fixture
def dotdrunc_data():
    return dotdrunc_json


@pytest.fixture
def dotdrunc_file():
    with tempfile.NamedTemporaryFile(delete=True, mode="w") as f:
        f.write(json.dumps(dotdrunc_json))
        f.flush()
        with setenv("DOTDRUNC_JSON", f.name):
            yield f.name
