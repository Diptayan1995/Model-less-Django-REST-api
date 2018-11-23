from rest_framework import serializers
'''





class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    email = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)

    def create(self, validated_data):
        #print (validated_data)
        return Task(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
'''