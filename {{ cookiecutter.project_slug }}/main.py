import os


# Flows
from core.processing.ingestion import flow_ingestion

# from core.processing.transformation import flow_transformation
# from core.processing.loading import flow_loading


def main():
    """
    Main function to run the flows
    """

    # Run the flow
    flow_ingestion()
    # flow_transformation()
    # flow_loading()


if __name__ == "__main__":
    main()
