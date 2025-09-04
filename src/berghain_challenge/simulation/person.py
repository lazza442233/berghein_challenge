class Person:
    """
    Represents a person arriving at the venue.

    Attributes:
        attributes (dict): A dictionary of binary attributes, e.g.,
                           {'local': True, 'all_black': False}.
    """

    def __init__(self, attributes: dict[str, bool]):
        if not isinstance(attributes, dict):
            raise TypeError("attributes must be a dictionary")

        self.attributes = attributes

    def __repr__(self) -> str:
        return f"Person(attributes={self.attributes})"
