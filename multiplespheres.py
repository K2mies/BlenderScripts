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
        if (checkForName(obj, "RandomSphere")):
            distance = calculateDistance(base_obj.location, obj.location)
            if distance > 0 and distance > max_distance:
                max_distance = distance
    return max_distance

#Function to calculate the Min distance from object between all other objects
def calculateMinDistanceFromObjects(base_obj, objs):
    min_distance = calculateMaxDistanceFromObjects(base_obj, objs)
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
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
        if (checkForName(obj, "RandomSphere")):
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
#Function to set all sphere objects to smooth shading
def smoothShadeAll(objs):
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
            for f in obj.data.polygons:
                f.use_smooth = True

#Function to create a bounding box based oin max loc range
def createBoundingBox(max_loc_range, target_collection):
        bpy.ops.mesh.primitive_cube_add(align = 'WORLD', location = Vector((0, 0, 0)))
        new_box = bpy.context.active_object
        new_box.dimensions = Vector((max_loc_range * 2, max_loc_range * 2, max_loc_range * 2))
        new_box.name = "Bounding_Box"
        new_box.display_type = 'WIRE'
        default_collection = bpy.context.scene.collection
        default_collection.objects.unlink(new_box)
        target_collection.objects.link(new_box)

#Function to check if object name containts 'name'   
def checkForName(obj, name):
    if name in obj.name:
        return True
    else:
        return False

# Function to check if sphere is out of bounds
def isSphereOutofBounds(obj, max_loc_range): 
    radius = obj.dimensions[0] / 2
    pos_distance_x = obj.location[0] + radius
    pos_distance_y = obj.location[1] + radius
    pos_distance_z = obj.location[2] + radius
    neg_distance_x = obj.location[0] - radius
    neg_distance_y = obj.location[1] - radius
    neg_distance_z = obj.location[2] - radius
    if pos_distance_x >= max_loc_range or neg_distance_x <= -max_loc_range:
        return True
    if pos_distance_y >= max_loc_range or neg_distance_y <= -max_loc_range:
        return True
    if pos_distance_z >= max_loc_range or neg_distance_z <= -max_loc_range:
        return True
    return False

#If an axis is out of bounds then it gets moved inside the bounds    
def moveOutOfBounds(obj, max_loc_range):
    #X===================================================
    #+x..x positive
    distance = obj.location[0] + (obj.dimensions[0] / 2)
    if distance >= max_loc_range:
        print(f"obj: {obj.name} moved on x+")
        obj.location[0] -= distance - max_loc_range
    #-x..x negative
    distance = obj.location[0] - (obj.dimensions[0] / 2)
    if distance <= -max_loc_range:
        print(f"obj: {obj.name} moved on x-")
        obj.location[0] -= distance - -max_loc_range
    #Y===================================================
    #+y..y positive
    distance = obj.location[1] + (obj.dimensions[1] / 2)
    if distance >= max_loc_range:
        print(f"obj: {obj.name} moved on y+")
        obj.location[1] -= distance - max_loc_range
    #-y..y negative 
    distance = obj.location[1] - (obj.dimensions[1] / 2)
    if distance <= -max_loc_range:
        print(f"obj: {obj.name} moved on y-")
        obj.location[1] -= distance - -max_loc_range
    #Z===================================================
    #+z..z positive
    distance = obj.location[2] + (obj.dimensions[2] / 2)
    if distance >= max_loc_range:
        print(f"obj: {obj.name} moved on z+")
        obj.location[2] -= distance - max_loc_range
    #-z..z negative 
    distance = obj.location[2] - (obj.dimensions[2] / 2)
    if distance <= -max_loc_range:
        print(f"obj: {obj.name} moved on z-")
        obj.location[2] -= distance - -max_loc_range

# Function to check if object is out of bounds, if it is then moves the object inbounds
def moveOutofBoundsObjects(objs, max_loc_range):
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
            if (isSphereOutofBounds(obj, max_loc_range)):
                print(f"Sphere {obj.name} is out of bounds")
                moveOutOfBounds(obj, max_loc_range)
    
# Function to create all the randomised spheres     
def createSpheres(max_loc_range, radius, n_spheres, target_collection, collection_name):
    #createBoundingBox(max_loc_range, target_collection)
    #max_loc_range *= 0.5
#    print("max loc range: ", max_loc_range)
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

def generateRandomSpheres(min_count = 1, max_count = 20, radius = 1.0, max_loc_range = 20.0, collection_name = "SPHERES"):
    
    #lets randomize the size of the bounding box
    max_loc_range = random.uniform(5, max_loc_range)
    
    #Create collection if it does not exist already
    target_collection = checkAndCreateCollection(collection_name)
        
    #set random number of spheres
    n_spheres = random.randint(min_count, max_count)
    print(f"Generating {n_spheres} spheres...")
    
    # Deselect all objects to ensure only the new spheres are selected
    bpy.ops.object.select_all(action='DESELECT')
    
    #create the bounding box
    createBoundingBox(max_loc_range, target_collection)
    
    #max_loc_range *= 0.5
    #create the spheres and add them to the collection
    createSpheres(max_loc_range, radius, n_spheres, target_collection, collection_name)
    
    #grab object array
    objs = bpy.data.collections['SPHERES'].objects
    
    #set diameter for all speres
    setDiametersForAll(objs)
    
    # -------------------------------------------------------------
    # FIX: Force Blender to update the dimensions before checking bounds!
    bpy.context.view_layer.update() 
    # 
    
    #Move objects that are out of bounds inside the bounding box
    moveOutofBoundsObjects(objs, max_loc_range)
    
    #reset diameter for all speres (stops overlap of offsets)
    setDiametersForAll(objs)
    
    #add smooth shading to all the objects
    smoothShadeAll(objs)

    # Deselect all objects to ensure only the bounding box is selected(for visual purposes)
    bpy.ops.object.select_all(action='DESELECT')
    
    #Set the bounding box to selected
    bpy.data.collections['SPHERES'].objects['Bounding_Box'].select_set(True)

#The main function executes here
generateRandomSpheres()