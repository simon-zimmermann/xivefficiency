from sqlmodel import SQLModel, create_engine

SQLModel.model_config['protected_namespaces'] = ()
engine = create_engine("sqlite:///resources/RESTingway.db")  # TODO use config file
