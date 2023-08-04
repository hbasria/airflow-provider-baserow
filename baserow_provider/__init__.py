__version__ = "1.0.0"

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-provider-baserow",  # Required
        "name": "Sample",  # Required
        "description": "A baserow provider for Apache Airflow.",  # Required
        "connection-types": [
            {
                "connection-type": "baserow",
                "hook-class-name": "baserow_provider.hooks.baserow.BaserowHook"
            }
        ],
        "versions": [__version__],  # Required
    }
