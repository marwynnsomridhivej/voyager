from typing import List, Union


class GenelabMission(object):
    __slots__ = [
        '_start_date',
        '_end_date',
        '_name',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._start_date = data.get("Start Date")
        self._end_date = data.get("End Date")
        self._name = data.get("Name")
        self._data = data

    @property
    def start_date(self) -> str:
        return self._start_date

    @property
    def end_date(self) -> str:
        return self._end_date

    @property
    def name(self) -> str:
        return self._name

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "GenelabMission":
        return cls(data)


class GenelabStudyPerson(object):
    __slots__ = [
        '_first_name',
        '_last_name',
        '_mid_init',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._first_name = data.get("First Name")
        self._last_name = data.get("Last Name")
        self._mid_init = data.get("Middle Initials")
        self._data = data

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def middle_initial(self) -> str:
        return self._mid_init

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "GenelabStudyPerson":
        return cls(data)


class GenelabSource(object):
    __slots__ = [
        '_auth_source_url',
        '_links',
        '_flight_program',
        '_mission',
        '_material_type',
        '_factor_value',
        '_accession',
        '_st_identifier',
        '_st_protocol_name',
        '_st_assay_tech_type',
        '_acknowledgements',
        '_st_assay_tech_platform',
        '_st_person',
        '_st_protocol_type',
        '_space_program',
        '_st_title',
        '_st_factor_type',
        '_st_pub_release_date',
        '_parameter_value',
        '_thumbnail',
        '_st_factor_name',
        '_st_assay_measure_type',
        '_proj_type',
        '_proj_identifier',
        '_data_source_accession',
        '_data_source_type',
        '_proj_title',
        '_st_funding_agency',
        '_st_protocol_description',
        '_expr_platform',
        '_characteristics',
        '_st_grant_number',
        '_st_pub_author_list',
        '_proj_link',
        '_st_pub_title',
        '_managing_nasa_center',
        '_st_description',
        '_organism',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._auth_source_url = data.get("Authoritative Source URL")
        self._links = data.get("links")
        self._flight_program = data.get("Flight Program")
        self._mission = GenelabMission(data.get("Mission"))
        self._material_type = data.get("Material Type")
        self._factor_value = data.get("Factor Value")
        self._accession = data.get("Accession")
        self._st_identifier = data.get("Study Identifier")
        self._st_protocol_name = data.get("Study Protocol Name")
        self._st_assay_tech_type = data.get("Study Assay Technology Type")
        self._acknowledgements = data.get("Acknowledgements")
        self._st_assay_tech_platform = data.get("Study Assay Technology Platform")
        self._st_person = GenelabStudyPerson(data.get("Study Person"))
        self._st_protocol_type = data.get("Study Protocol Type")
        self._space_program = data.get("Space Program")
        self._st_title = data.get("Study Title")
        self._st_factor_type = data.get("Study Factor Type")
        self._st_pub_release_date = data.get("Study Public Release Date")
        self._parameter_value = data.get("Parameter Value")
        self._thumbnail = data.get("thumbnail")
        self._st_factor_name = data.get("Study Factor Name")
        self._st_assay_measure_type = data.get("Study Assay Measurement Type")
        self._proj_type = data.get("Project Type")
        self._proj_identifier = data.get("Project Identifier")
        self._data_source_accession = data.get("Data Source Accession")
        self._data_source_type = data.get("Data Source Type")
        self._proj_title = data.get("Project Title")
        self._st_funding_agency = data.get("Study Funding Agency")
        self._st_protocol_description = data.get("Study Protocol Description")
        self._expr_platform = data.get("Experiment Platform")
        self._characteristics = data.get("Characteristics")
        self._st_grant_number = data.get("Study Grant Number")
        self._st_pub_author_list = data.get("Study Publication Author List")
        self._proj_link = data.get("Project Link")
        self._st_pub_title = data.get("Study Publication Title")
        self._managing_nasa_center = data.get("Managing NASA Center")
        self._st_description = data.get("Study Description")
        self._organism = data.get("organism")
        self._data = data

    @property
    def authoritative_source_url(self) -> str:
        return self._auth_source_url

    @property
    def auth_source_url(self) -> Union[str, None]:
        return self.authoritative_source_url

    @property
    def links(self) -> Union[List[str], None]:
        return self._links

    @property
    def flight_program(self) -> Union[str, None]:
        return self._flight_program

    @property
    def mission(self) -> GenelabMission:
        return self._mission

    @property
    def material_type(self) -> Union[str, None]:
        return self._material_type

    @property
    def factor_value(self) -> Union[List[str], None]:
        return self._factor_value

    @property
    def accession(self) -> Union[str, None]:
        return self._accession

    @property
    def study_identifier(self) -> Union[str, None]:
        return self._st_identifier

    @property
    def study_id(self) -> Union[str, None]:
        return self.study_identifier

    @property
    def study_protocol_name(self) -> Union[str, None]:
        return self._st_protocol_name

    @property
    def study_assay_technology_type(self) -> Union[str, None]:
        return self._st_assay_tech_type

    @property
    def study_assay_tech_type(self) -> Union[str, None]:
        return self.study_assay_technology_type

    @property
    def acknowledgements(self) -> Union[str, None]:
        return self._acknowledgements

    @property
    def study_assay_technology_platform(self) -> Union[str, None]:
        return self._st_assay_tech_platform

    @property
    def study_assay_tech_platform(self) -> Union[str, None]:
        return self.study_assay_technology_platform

    @property
    def study_person(self) -> GenelabStudyPerson:
        return self._st_person

    @property
    def person(self) -> GenelabStudyPerson:
        return self.study_person

    @property
    def study_protocol_type(self) -> Union[str, None]:
        return self._st_protocol_type

    @property
    def space_program(self) -> Union[str, None]:
        return self._space_program

    @property
    def study_title(self) -> Union[str, None]:
        return self._st_title

    @property
    def study_factor_type(self) -> Union[List[str], None]:
        return self._st_factor_type

    @property
    def study_public_release_date(self) -> Union[int, None]:
        return self._st_pub_release_date

    @property
    def study_pub_rel_date(self) -> Union[int, None]:
        return self.study_public_release_date

    @property
    def parameter_value(self) -> Union[List[str], None]:
        return self._parameter_value

    @property
    def param_value(self) -> Union[List[str], None]:
        return self.parameter_value

    @property
    def thumbnail(self) -> Union[str, None]:
        return self._thumbnail

    @property
    def study_factor_name(self) -> Union[str, None]:
        return self._st_factor_name

    @property
    def study_assay_measurement_type(self) -> Union[str, None]:
        return self._st_assay_measure_type

    @property
    def study_assay_meas_type(self) -> Union[str, None]:
        return self.study_assay_measurement_type

    @property
    def project_type(self) -> Union[str, None]:
        return self._proj_type

    @property
    def project_identifier(self) -> Union[str, None]:
        return self._proj_identifier

    @property
    def project_id(self) -> Union[str, None]:
        return self.project_identifier

    @property
    def data_source_accession(self) -> Union[str, None]:
        return self._data_source_accession

    @property
    def data_source_type(self) -> Union[str, None]:
        return self._data_source_type

    @property
    def project_title(self) -> Union[str, None]:
        return self._proj_title

    @property
    def study_funding_agency(self) -> Union[str, None]:
        return self._st_funding_agency

    @property
    def study_protocol_description(self) -> Union[str, None]:
        return self._st_protocol_description

    @property
    def study_protocol_desc(self) -> Union[str, None]:
        return self.study_protocol_description

    @property
    def experiment_platform(self) -> Union[str, None]:
        return self._expr_platform

    @property
    def characteristics(self) -> Union[List[str], None]:
        return self._characteristics

    @property
    def study_grant_number(self) -> Union[str, None]:
        return self._st_grant_number

    @property
    def study_publication_author_list(self) -> Union[str, None]:
        return self._st_pub_author_list

    @property
    def study_pub_authors(self) -> Union[str, None]:
        return self.study_publication_author_list

    @property
    def project_link(self) -> Union[str, None]:
        return self._proj_link

    @property
    def study_publication_title(self) -> Union[str, None]:
        return self._st_pub_title

    @property
    def study_pub_title(self) -> Union[str, None]:
        return self.study_publication_title

    @property
    def managing_nasa_center(self) -> Union[str, None]:
        return self._managing_nasa_center

    @property
    def study_description(self) -> Union[str, None]:
        return self._st_description

    @property
    def study_desc(self) -> Union[str, None]:
        return self.study_description

    @property
    def organism(self) -> Union[List[str], None]:
        return self._organism

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "GenelabSource":
        return cls(data)


class GenelabHighlight(object):
    __slots__ = [
        '_all',
        '_data',
    ]

    def __init__(self, data: dict) -> None:
        self._all = data.get("all")
        self._data = data

    @property
    def all(self) -> Union[List[str], None]:
        return self._all

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "GenelabHighlight":
        return cls(data)


class GenelabHit(object):
    __slots__ = [
        '_index',
        '_type',
        '_id',
        '_score',
        '_data',
    ]
    _cache = {}

    def __init__(self, data: dict) -> None:
        self._index = data.get("_index")
        self._type = data.get("_type")
        self._id = data.get("_id")
        self._score = data.get("_score")
        self._data = data

    @property
    def index(self) -> str:
        return self._index

    @property
    def type(self) -> str:
        return self._type

    @property
    def id(self) -> str:
        return self._id

    @property
    def score(self) -> float:
        return self._score

    @property
    def source(self) -> GenelabSource:
        if (src := f"{self}source") not in self._cache:
            self._cache[src] = GenelabSource(self._data.get("_source"))
        return self._cache[src]

    @property
    def highlight(self) -> GenelabHighlight:
        if (hl := f"{self}highlight") not in self._cache:
            self._cache[hl] = GenelabHighlight(self._data.get("highlight"))
        return self._cache[hl]

    @property
    def to_dict(self) -> dict:
        return self._data

    @classmethod
    def from_dict(cls, data: dict) -> "GenelabHit":
        return cls(data)
