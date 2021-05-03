import pytest

from dhalsim.parser.config_parser import ConfigParser, EmptyConfigError, MissingValueError


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        ConfigParser("non_existing_path.yaml")


def test_imp_path_good(tmpdir):
    c = tmpdir.join("config.yaml")
    inp_file = tmpdir.join("test.inp")
    inp_file.write("some: thing")
    c.write("inp_file: test.inp")
    parser = ConfigParser(str(c))
    assert parser.inp_path == str(tmpdir.join("test.inp"))


def test_imp_path_missing(tmpdir):
    c = tmpdir.join("config.yaml")
    c.write("something: else")
    parser = ConfigParser(str(c))
    with pytest.raises(MissingValueError):
        parser.inp_path()


def test_imp_path_not_found(tmpdir):
    c = tmpdir.join("config.yaml")
    c.write("inp_file: test.inp")
    parser = ConfigParser(str(c))
    with pytest.raises(FileNotFoundError):
        parser.inp_path()


def test_empty_config(tmpdir):
    c = tmpdir.join("config.yaml")
    c.write(" ")
    with pytest.raises(EmptyConfigError):
        ConfigParser(str(c))


def test_cpa_path_good(tmpdir):
    c = tmpdir.join("config.yaml")
    inp_file = tmpdir.join("test.yaml")
    inp_file.write("some: thing")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    assert parser.cpa_path == str(tmpdir.join("test.yaml"))


def test_cpa_path_missing(tmpdir):
    c = tmpdir.join("config.yaml")
    c.write("something: else")
    parser = ConfigParser(str(c))
    with pytest.raises(MissingValueError):
        parser.cpa_path()


def test_cpa_path_not_found(tmpdir):
    c = tmpdir.join("config.yaml")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    with pytest.raises(FileNotFoundError):
        parser.cpa_path()


def test_cpa_data_path_good(tmpdir):
    c = tmpdir.join("config.yaml")
    cpa_file = tmpdir.join("test.yaml")
    cpa_file.write("some: thing")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    assert parser.cpa_data == {"some": "thing"}


def test_cpa_data_path_missing(tmpdir):
    c = tmpdir.join("config.yaml")
    c.write("something: else")
    parser = ConfigParser(str(c))
    with pytest.raises(MissingValueError):
        parser.cpa_data()


def test_cpa_data_path_not_found(tmpdir):
    c = tmpdir.join("config.yaml")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    with pytest.raises(FileNotFoundError):
        parser.cpa_data()


def test_generate_plc_config_no_plcs(tmpdir):
    c = tmpdir.join("config.yaml")
    cpa_file = tmpdir.join("test.yaml")
    cpa_file.write("some: thing")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    assert len(parser.generate_plc_configs()) == 0


def test_generate_plc_config_plcs_empty(tmpdir):
    c = tmpdir.join("config.yaml")
    cpa_file = tmpdir.join("test.yaml")
    cpa_file.write("plcs: []")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    assert len(parser.generate_plc_configs()) == 0


def test_generate_plc_config_plcs_normal(tmpdir):
    c = tmpdir.join("config.yaml")
    cpa_file = tmpdir.join("test.yaml")
    cpa_file.write("""plcs:
  - name: PLC1
    sensors:
      - T1
    actuators:
      - P_RAW1
      - V_PUB
  - name: PLC2
    sensors:
      - T2
      - T3
    actuators:
      - V_ER2i""")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    result = parser.generate_plc_configs()
    assert len(result) == 2
    #PLC 1
    assert result[0].name == "PLC1"
    assert result[0].sensors == ["T1"]
    assert result[0].actuators == ["P_RAW1", "V_PUB"]
    # PLC 2
    assert result[1].name == "PLC2"
    assert result[1].sensors == ["T2", "T3"]
    assert result[1].actuators == ["V_ER2i"]


def test_generate_plc_config_plcs_empty_sensor(tmpdir):
    c = tmpdir.join("config.yaml")
    cpa_file = tmpdir.join("test.yaml")
    cpa_file.write("""plcs:
  - name: PLC1
    sensors:
    actuators:
      - P_RAW1
      - V_PUB""")
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    result = parser.generate_plc_configs()
    #PLC 1
    assert result[0].name == "PLC1"
    assert result[0].sensors == []
    assert result[0].actuators == ["P_RAW1", "V_PUB"]


def test_generate_plc_config_plcs_empty_actuator(tmpdir):
    c = tmpdir.join("config.yaml")
    cpa_file = tmpdir.join("test.yaml")
    cpa_file.write("""plcs:
  - name: PLC1
    sensors: 
      - T1
    """)
    c.write("cpa_file: test.yaml")
    parser = ConfigParser(str(c))
    result = parser.generate_plc_configs()
    #PLC 1
    assert result[0].name == "PLC1"
    assert result[0].sensors == ["T1"]
    assert result[0].actuators == []

