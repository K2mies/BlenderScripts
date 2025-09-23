#ok how do we get the distance between two points
import bpy
import math
import random
from mathutils import Vector

#Function to calculate the square root of a number
def sqr(number):
    return number ** 2

#Function to calculate teh distance between two 3d Vectors
def calculateDistance(a, b):
    distance = (a - b).length
    return distance

#Function to calculate the Max distance from object between all other objects
def calculateMaxDistanceFromObjects(base_obj, objs):
    max_distance = 0
    for obj in objs:
        distance = calculateDistance(base_obj.location, obj.location)
        if distance > 0 and distance > max_distance:
            max_distance = distance
    return max_distance

#Function to calculate the Min distance from object between all other objects
def calculateMinDistanceFromObjects(base_obj, objs):
    min_distance = calculateMaxDistanceFromObjects(base_obj, objs)
    for obj in objs:
        distance = calculateDistance(base_obj.location, obj.location)
        if distance < min_distance and distance > 0:
            min_distance = distance
    return min_distance    

#Function to change the diameter of a sphere to the distance
def setDiameter(obj, diameter):
    dimensions = Vector((diameter, diameter, diameter))
    obj.dimensions = dimensions

#Function to change the diameter for all spheres
def setDiametersForAll(objs):
    for obj in objs:
        distance = calculateMinDistanceFromObjects(obj, objs)
        setDiameter(obj, distance)

#Function to check if SPHERES collection exists and if not to create it
def checkAndCreateCollection(collection_name):
    #check if target collection exists, if not then create it
    if collection_name in bpy.data.collections:
        target_collection = bpy.data.collections[collection_name]
        objects_to_delete = target_collection.objects
        for obj in objects_to_delete:
            bpy.data.objects.remove(obj, do_unlink=True)
        return target_collection
    #Otherwise create the collection and link it
    else:
        target_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(target_collection)
        print(f"Created new collection: '{collection_name}'")
        return target_collection
    
def createSpheres(max_loc_range, radius, n_spheres, target_collection, collection_name):
    for i in range(n_spheres):
        #Create the random position coordinates
        loc_x = random.uniform(-max_loc_range, max_loc_range)
        loc_y = random.uniform(-max_loc_range, max_loc_range)
        loc_z = random.uniform(-max_loc_range, max_loc_range)
        
        #Create the sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius = 1.0, location = (loc_x, loc_y, loc_z))
        
        # Get a reference to the newly created object
        new_sphere = bpy.context.active_object
        new_sphere.name = f"RandomSphere_{i}"
        
        # 5. Link the new sphere to the target collection
        # First, unlink from the default scene collection
        default_collection = bpy.context.scene.collection
        default_collection.objects.unlink(new_sphere)
        
         # Then, link it to our target collection
        target_collection.objects.link(new_sphere)
        print(f"Created sphere '{new_sphere.name}' in '{collection_name}' with radius {radius:.2f}")

def generateRandomSpheres(min_count = 1, max_count = 20, radius = 1.0, max_loc_range = 10.0, collection_name = "SPHERES"):
    
    #Create collection if it does not exist already
    target_collection = checkAndCreateCollection(collection_name)
    
    #set random number of spheres
    n_spheres = random.randint(min_count, max_count)
    print(f"Generating {n_spheres} spheres...")
    
    # Deselect all objects to ensure only the new spheres are selected
    bpy.ops.object.select_all(action='DESELECT')
    
    #create the spheres and add them to the collection
    createSpheres(max_loc_range, radius, n_spheres, target_collection, collection_name)
    
    #grab object array
    objs = bpy.data.collections['SPHERES'].objects
    
    #set diameter for all speres
    setDiametersForAll(objs)

generateRandomSpheres()