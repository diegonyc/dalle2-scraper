"""
Implementation of the `storage` abstraction using Algolia.
"""

from .storage import GenerationRepository

from algoliasearch.search_client import SearchClient


class AlgoliaGenerationRepository(GenerationRepository):
    """
    Repository instance that points to an Algolia Index.  That index will be 
    where all the generations will be stored.
    """

    def __init__(self, app_id, api_key, generation_index) -> None:
        super().__init__()

        self._client = SearchClient.create(app_id=app_id, api_key=api_key)
        self._generation_index = self._client.init_index(generation_index)

    def store_generation(self, generation):
        """
        Store a generation in the Algolia Index that was configured when the
        repository was initialized.
        """
        # required attribute assertion
        super().store_generation(generation)

        print(f"Saving generation to Algolia. ID = {generation['objectID']}")
        self._generation_index.save_object(generation).wait()
        print("Done.\n")
    
    def get_generation(self, object_id):
        super().get_generation(object_id)
        return self._generation_index.get_object(object_id=object_id)
