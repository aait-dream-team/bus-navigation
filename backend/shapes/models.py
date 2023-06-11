from django.db import models

class Shape(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    shape_pt_lat = models.DecimalField(max_digits=9, decimal_places=6)
    shape_pt_lon = models.DecimalField(max_digits=9, decimal_places=6)
    shape_pt_sequence = models.IntegerField()
    shape_dist_traveled = models.DecimalField(max_digits=9, decimal_places=6)

    # define a str method that returns the shape id and sequence
    def __str__(self):
        return f'Shape {self.shape_id} - Sequence {self.shape_pt_sequence}'
