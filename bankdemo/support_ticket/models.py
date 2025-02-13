from django.db import models

# Create your models here.
class SupportModel (models.Model):

    Status = (
              ("open","Open"),
              ( "in progress", "In progress"), 
              ("resolved", "Resolved")
              )

    user = models.ForeignKey('users.NewUser', on_delete= models.CASCADE)
    subject = models.CharField(max_length= 70)
    description=models.TextField() 
    status = models.CharField(max_length= 20, choices=Status, blank=False, null=False, default="open")
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject}"