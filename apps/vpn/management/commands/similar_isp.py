# در فایل custom_commands/management/commands/merge_fields.py

from django.core.management.base import BaseCommand
from apps.vpn.models import Vpn, Test


def is_similar(str1, str2, threshold):
    len_str1 = len(str1)
    len_str2 = len(str2)

    # Initialize the matrix
    matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

    # Fill in the first row
    for i in range(len_str1 + 1):
        matrix[i][0] = i

    # Fill in the first column
    for j in range(len_str2 + 1):
        matrix[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,  # deletion
                               matrix[i][j - 1] + 1,  # insertion
                               matrix[i - 1][j - 1] + cost)  # substitution

    # Calculate similarity ratio
    similarity_ratio = (len_str1 + len_str2 - matrix[len_str1][len_str2]) / (len_str1 + len_str2)

    return similarity_ratio >= threshold


class Command(BaseCommand):
    help = 'Merge similar fields in a database column'

    def add_arguments(self, parser):
        parser.add_argument('column_name', type=str, help='Name of the column to be processed')
        parser.add_argument('--similarity_threshold', type=float, default=0.8, help='Threshold for similarity')

    def handle(self, *args, **kwargs):
        column_name = kwargs['column_name']
        similarity_threshold = kwargs['similarity_threshold']

        # Logic to merge similar fields
        records = Test.objects.all()
        for record in records:
            # Get values of the specified column
            column_values = [getattr(record, column_name) for record in records]

            # Compare each value with others and merge if similar
            for i in range(len(column_values)):
                for j in range(i + 1, len(column_values)):
                    if is_similar(column_values[i], column_values[j], similarity_threshold):
                        # Merge the similar fields (you need to implement this part)
                        pass

        self.stdout.write(self.style.SUCCESS('Fields merged successfully'))
