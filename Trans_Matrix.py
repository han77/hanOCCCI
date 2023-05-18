import numpy as np

class Trans_Matrix:
    def __init__(self, rotation_angles, translation):
        """
        Initializes the Trans_Matrix class with rotation angles for each axis and translation vector.

        Args:
            rotation_angles (array-like): The rotation angles for each axis in radians. Shape: (3,).
            translation (array-like): The translation vector in 3D space. Shape: (3,).
        """
        self.rotation_angles = rotation_angles
        self.translation = translation
        self.rotation_matrices = self._create_rotation_matrices(rotation_angles)
        self.translation_matrix = self._create_translation_matrix(translation)
        self.transformation_matrix = self._create_transformation_matrix()

    def _create_rotation_matrices(self, rotation_angles):
        """
        Creates the rotation matrices for each axis using the given rotation angles.

        Args:
            rotation_angles (array-like): The rotation angles for each axis in radians. Shape: (3,).

        Returns:
            list: The list of 3x3 rotation matrices.
        """
        rotation_matrices = []
        for angle, axis in zip(rotation_angles, ['x', 'y', 'z']):
            rotation_matrix = self._create_rotation_matrix(axis, angle)
            rotation_matrices.append(rotation_matrix)
        return rotation_matrices

    def _create_rotation_matrix(self, rotation_axis, angle):
        """
        Creates the rotation matrix based on the rotation axis and angle.

        Args:
            rotation_axis (str): The rotation axis ('x', 'y', or 'z').
            angle (float): The rotation angle in radians.

        Returns:
            array-like: The 3x3 rotation matrix.
        """
        if rotation_axis == 'x':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)]
            ])
        elif rotation_axis == 'y':
            rotation_matrix = np.array([
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)]
            ])
        elif rotation_axis == 'z':
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]
            ])
        else:
            raise ValueError("Invalid rotation axis. Please choose 'x', 'y', or 'z'.")
        
        return rotation_matrix

    def _create_translation_matrix(self, translation):
        """
        Creates the translation matrix using the given translation vector.

        Args:
            translation (array-like): The translation vector in 3D space. Shape: (3,).

        Returns:
            array-like: The 4x4 translation matrix.
        """
        translation_matrix = np.eye(4)
        translation_matrix[:3, 3] = translation
        return translation_matrix

    def _create_transformation_matrix(self):
        """
        Creates the transformation matrix by combining the rotation and translation matrices.

        Returns:
            array-like: The 4x4 transformation matrix.
        """
        transformation_matrix = np.eye(4)
        for rotation_matrix in self.rotation_matrices:
            transformation_matrix[:3, :3] = np.dot(transformation_matrix[:3, :3], rotation_matrix)
        transformation_matrix[:3, 3] = self.translation
        return transformation_matrix

    def transform_point(self, point):
        """
        Transforms a 3D point to the new coordinate system.

        Args:
            point (array-like): The 3D point to be transformed. Shape: (3,).

        Returns:
            array-like: The transformed 3D point.
        """
        homogeneous_point = np.append(point, 1)
        transformed_point = np.dot(self.transformation_matrix, homogeneous_point)[:3]
        return transformed_point
    