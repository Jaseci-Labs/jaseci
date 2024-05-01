from typing import Optional, Dict
from pathlib import Path
import os
import shutil
import uuid
import json


DEFAULT_RETENTION_COUNT = 10


class ModelManager:
    """
    A class for managing models, including saving, loading, deleting, and cleaning up old versions.

    Attributes:
        model_dir (str): The directory where the models are saved.
        metadata_file (str): The file path of the metadata file.

    Methods:
        __init__(self, model_dir: str): Initializes the ModelManager object.
        save_metadata(self): Saves the metadata to the metadata file.
        create_version_path(self, version_id: Optional[str] = None): Gets the save path for the model.
        get_version_path(self, version_id: Optional[str] = None): Gets the load path for the model.
        delete_model(self, version_id: str): Deletes the model with the specified version ID.
        get_version_ids(self): Gets a list of all version IDs, sorted by creation time.
        get_latest_version(self): Gets the version ID of the latest model.
        set_latest_version(self, version_id: Optional[str] = None): Sets the version ID of the latest model.
        cleanup_old_versions(self, retention_count: Optional[int] = None): Cleans up old models, keeping a specified number of versions.
    """

    def __init__(self, model_dir: str):
        """
        Initializes the ModelManager object.

        Args:
            model_dir (str): The directory where the models are saved.
        """
        self.model_dir = Path(model_dir)

        # Create the model directory if it doesn't exist
        self.model_dir.mkdir(parents=True, exist_ok=True)

        # Load the metadata if it exists, otherwise create an empty metadata dictionary
        self.metadata_file = self.model_dir / "metadata.json"
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "latest_version": "",
                "version_table": {},
                "version_count": 0,
            }
            self.save_metadata()

    def save_metadata(self):
        """
        Saves the metadata to the metadata file.
        """
        # Save the metadata dictionary to a JSON file
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f)

    def create_version_path(self, version_id: Optional[str] = None) -> Path:
        """
        Gets the save path for the model.

        Args:
            version_id (Optional[str]): The version ID of the model to save. If not specified, a new version ID will be generated.

        Returns:
            The path to the directory where the model should be saved.
        """
        # Generate a unique ID for the new model version if no ID is provided
        if version_id is None:
            version_id = str(uuid.uuid4())

        # Create a directory for the new model version
        version_path = self.model_dir / version_id
        version_path.mkdir(exist_ok=True)

        # Update the metadata dictionary with information about the new model version
        self.metadata["version_table"][version_id] = str(version_path)
        self.metadata["version_count"] += 1
        self.metadata["latest_version"] = version_id

        # Save the updated metadata dictionary
        self.save_metadata()

        # Clean up old model versions
        self.cleanup_old_versions()

        # Return the path to the new model version directory
        return version_path

    def get_version_path(self, version_id: Optional[str] = None) -> Optional[Path]:
        """
        Gets the load path for the model.

        Args:
            version_id (Optional[str]): The version ID of the model to load. If not specified, the latest version will be loaded.

        Returns:
            The path to the directory where the model is saved.
        """
        # If no version ID is provided, use the latest version ID from the metadata dictionary
        if version_id is None:
            version_id = self.metadata["latest_version"]

        # Look up the path to the specified model version in the metadata dictionary
        if version_id in self.metadata["version_table"]:
            load_path = Path(self.metadata["version_table"][version_id])
        else:
            load_path = None

        # Return the path to the specified model version directory, or None if the version ID is invalid
        return load_path

    def delete_model(self, version_id: str):
        """
        Deletes the directory for the specified model version and removes the model version from the metadata dictionary.

        Args:
            version_id (str): The ID of the model version to be deleted.

        Returns:
            None
        """
        # Delete the directory for the specified model version
        model_path = self.metadata["version_table"][version_id]
        shutil.rmtree(model_path)

        # Remove the model version from the metadata dictionary
        del self.metadata["version_table"][version_id]
        self.metadata["version_count"] -= 1
        if version_id == self.metadata["latest_version"]:
            self.metadata["latest_version"] = ""

        # Save the updated metadata dictionary
        self.save_metadata()

    def get_version_ids(self) -> Dict[str, int]:
        """
        Returns a dictionary that maps each model version ID to a rank based on creation time.

        Args:
            None

        Returns:
            Dict[str, int]: A dictionary that maps each model version ID to a rank based on creation time.
        """
        # Get a list of version IDs sorted by creation time
        version_ids = sorted(
            self.metadata["version_table"].keys(),
            key=lambda x: os.stat(self.metadata["version_table"][x]).st_ctime,
        )

        # Create a dictionary that maps each version ID to a rank based on creation time
        version_id_with_idx = {}
        for idx, version_id in enumerate(version_ids):
            version_id_with_idx[version_id] = idx + 1

        # Return the dictionary that maps version IDs to ranks
        return version_id_with_idx

    def get_latest_version(self) -> Optional[str]:
        """
        Returns the ID of the latest model version from the metadata dictionary.

        Args:
            None

        Returns:
            Optional[str]: The ID of the latest model version, or None if there are no model versions.
        """
        # Return the latest version ID from the metadata dictionary
        return self.metadata["latest_version"]

    def set_latest_version(self, version_id: Optional[str] = None) -> str:
        """
        Sets the ID of the latest model version in the metadata dictionary.

        Args:
            version_id (Optional[str]): The ID of the model version to set as the latest version. If None, sets the latest version to an empty string.

        Returns:
            str: The ID of the latest model version.
        """
        if version_id is None:
            # If version_id is None, set the latest version to an empty string
            self.metadata["latest_version"] = ""
        else:
            # If version_id is not None, check that it exists in the version table
            if version_id not in self.metadata["version_table"]:
                raise ValueError(f"Version {version_id} not found in version table")
            self.metadata["latest_version"] = version_id
        # Save the updated metadata dictionary
        self.save_metadata()
        # Return the latest version ID
        return self.metadata["latest_version"]

    def cleanup_old_versions(self, retention_count: Optional[int] = None):
        """
        Deletes old model versions that exceed the specified retention count, and keeps the specified number of most recent model versions.

        Args:
            retention_count (Optional[int]): The number of most recent model versions to retain. If None, uses the default retention count.

        Returns:
            None
        """
        if retention_count is None:
            # If retention_count is None, use the default retention count
            retention_count = DEFAULT_RETENTION_COUNT
        if self.metadata["version_count"] <= retention_count:
            # If the number of versions is less than or equal to the retention count, no cleanup is needed
            return
        # Get a list of version IDs sorted by creation time
        version_names = sorted(
            self.metadata["version_table"].keys(),
            key=lambda x: os.stat(self.metadata["version_table"][x]).st_ctime,
        )
        # Delete old versions starting from the oldest
        for version_id in version_names[:-retention_count]:
            try:
                # Try to delete the version directory
                self.delete_model(version_id)
            except Exception as e:
                # If there is an error, print a message but continue with the cleanup process
                print(f"Error deleting version {version_id}: {e}")
