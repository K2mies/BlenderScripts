#ok how do we get the distance between two points
import bpy
import math
import random
from mathutils import Vector
 
EPSILON = 1e-6
SAFETY = 0.99
 
#Function to calculate the distance between two 3d Vectors
def calculateDistance(a, b):
    distance = (a - b).length
    return distance
 
#Function to calculate the Max distance from object between all other objects
def calculateMaxDistanceFromObjects(base_obj, objs):
    max_distance = 0
    for obj in objs:
        if obj == base_obj:
            continue
        if (checkForName(obj, "RandomSphere")):
            distance = calculateDistance(base_obj.location, obj.location)
            if distance > max_distance:
                max_distance = distance
    return max_distance
 
#Function to calculate the Min distance from object between all other objects
def calculateMinDistanceFromObjects(base_obj, objs):
    min_distance = calculateMaxDistanceFromObjects(base_obj, objs)
    for obj in objs:
        if obj == base_obj:
            continue
        if (checkForName(obj, "RandomSphere")):
            distance = calculateDistance(base_obj.location, obj.location)
            if distance < min_distance:
                min_distance = distance
    return min_distance
 
#Function to change the diameter of a sphere to the distance
def setDiameter(obj, diameter):
    dimensions = Vector((diameter, diameter, diameter))
    obj.dimensions = dimensions
    bpy.context.view_layer.update() 
 
#Function to change the diameter for all spheres
def setDiametersForAll(objs):
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
            distance = calculateMinDistanceFromObjects(obj, objs)
            setDiameter(obj, distance * SAFETY)
            bpy.context.view_layer.update()
 
# Function to return he closest obj to the base object            
def getClosestObjAndDistance(base_obj, objs):
    min_distance = calculateMaxDistanceFromObjects(base_obj, objs)
    closest_obj = None
    for obj in objs:
        if obj == base_obj:
            continue
        if (checkForName(obj, "RandomSphere")):
            distance = calculateDistance(base_obj.location, obj.location)
            if distance < min_distance:
                closest_obj = obj
                min_distance = distance
    return closest_obj, min_distance
 
#Function to check if there is still room to expand one of the spheres
def isCombinedRadiUnderDistance(obj, closest_obj, distance):
    if ((obj.dimensions[0] / 2) + (closest_obj.dimensions[0] / 2) < distance - EPSILON):
        return True
    else:
        return False
    
#set the diameter based on gap between objects
def fillDiameterGap(obj, closest_obj, distance):
    radi = (obj.dimensions[0] / 2) + (closest_obj.dimensions[0] / 2)
    gap = distance - radi
#    safe_expansion = expansion * 0.5
    if gap > EPSILON:
        expansion = gap * 0.5
        setDiameter(obj, obj.dimensions[0] + expansion * SAFETY)
        bpy.context.view_layer.update() 
 
#Function to check if SPHERES collection exists and if not to create it
def checkAndCreateCollection(collection_name):
    #check if target collection exists, if notp then create it
    #if it already exists then delete it's contents
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
        #print(f"Created new collection: '{collection_name}'")
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
        bpy.context.view_layer.update() 
 
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
        #print(f"obj: {obj.name} moved on x+")
        obj.location[0] -= distance - max_loc_range
        bpy.context.view_layer.update()
    #-x..x negative
    distance = obj.location[0] - (obj.dimensions[0] / 2)
    if distance <= -max_loc_range:
        #print(f"obj: {obj.name} moved on x-")
        obj.location[0] -= distance - -max_loc_range
        bpy.context.view_layer.update()
    #Y===================================================
    #+y..y positive
    distance = obj.location[1] + (obj.dimensions[1] / 2)
    if distance >= max_loc_range:
        #print(f"obj: {obj.name} moved on y+")
        obj.location[1] -= distance - max_loc_range
        bpy.context.view_layer.update()
    #-y..y negative 
    distance = obj.location[1] - (obj.dimensions[1] / 2)
    if distance <= -max_loc_range:
        #print(f"obj: {obj.name} moved on y-")
        obj.location[1] -= distance - -max_loc_range
        bpy.context.view_layer.update()
    #Z===================================================
    #+z..z positive
    distance = obj.location[2] + (obj.dimensions[2] / 2)
    if distance >= max_loc_range:
        #print(f"obj: {obj.name} moved on z+")
        obj.location[2] -= distance - max_loc_range
        bpy.context.view_layer.update()
    #-z..z negative 
    distance = obj.location[2] - (obj.dimensions[2] / 2)
    if distance <= -max_loc_range:
        #print(f"obj: {obj.name} moved on z-")
        obj.location[2] -= distance - -max_loc_range
        bpy.context.view_layer.update()
 
# Function to check if object is out of bounds, if it is then moves the object inbounds
def moveOutofBoundsObjects(objs, max_loc_range):
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
            if (isSphereOutofBounds(obj, max_loc_range)):
                #print(f"Sphere {obj.name} is out of bounds")
                moveOutOfBounds(obj, max_loc_range)
                bpy.context.view_layer.update()
 
# Function to reduce Diameter by reduction
def reduceDiameter(obj, reduction):
    reduction_vector = Vector((reduction, reduction, reduction))
    obj.dimensions -= reduction_vector
    bpy.context.view_layer.update() 
 
#function to check if there is any overlap between any of the cylinders and then correct it
def fixOverlap(base_obj, objs):
    for obj in objs:
        if obj == base_obj:
            continue
        if (checkForName(obj, "RandomSphere")):
            distance = calculateDistance(base_obj.location, obj.location)
            radi = (base_obj.dimensions[0] / 2) + (obj.dimensions[0] / 2)
            difference = radi - distance
            if difference > EPSILON:
                reduceDiameter(base_obj, difference / 2)
                reduceDiameter(obj, difference / 2)
                bpy.context.view_layer.update()
                    
 
#Functiont to fix all overlaps
def fixAllOverlaps(objs):
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
            fixOverlap(obj, objs)
 
#Function to check if there is overlap between one object and all other objects
def isOverlap(base_obj, objs):
    for obj in objs:
        if obj == base_obj:
            continue
        if (checkForName(obj, "RandomSphere")):
            distance = calculateDistance(base_obj.location, obj.location)
            radi = (base_obj.dimensions[0] / 2) + (obj.dimensions[0] / 2)
            if radi > distance + EPSILON:
                return True
    return False
 
#Function to check if there is any overlap still in the simulation            
def isSphereOverlap(objs):
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
            if (isOverlap(obj, objs)):
                #print("There is still overlap in the simulation")
                return True
    #print("There is no overlap in the simulation")
    return False
            
            
# Function to create all the randomised spheres     
def createSpheres(max_loc_range, radius, n_spheres, target_collection, collection_name):
    for i in range(n_spheres):
        #Create the random position coordinates
        loc_x = random.uniform(-max_loc_range, max_loc_range)
        loc_y = random.uniform(-max_loc_range, max_loc_range)
        loc_z = random.uniform(-max_loc_range, max_loc_range)
 
        #Create the sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius = radius, location = (loc_x, loc_y, loc_z))
        
        # Get a reference to the newly created object
        new_sphere = bpy.context.active_object
        new_sphere.name = f"RandomSphere_{i}"
        
        # Link the new sphere to the target collection
        # First, unlink from the default scene collection
        default_collection = bpy.context.scene.collection
        default_collection.objects.unlink(new_sphere)
        
         # Then, link it to our target collection
        target_collection.objects.link(new_sphere)
        #print(f"Created sphere '{new_sphere.name}' in '{collection_name}' with radius {radius:.2f}")
def isOverlap(base_obj, objs):
    for obj in objs:
        if obj == base_obj:
            continue
        if (checkForName(obj, "RandomSphere")):
            distance = calculateDistance(base_obj.location, obj.location)
            radi = (base_obj.dimensions[0] / 2) + (obj.dimensions[0] / 2)
            if radi > distance + EPSILON:
                return True
    return False

#Function to check if there is any overlap still in the simulation            
def isSphereOverlap(objs):
    for obj in objs:
        if (checkForName(obj, "RandomSphere")):
            if (isOverlap(obj, objs)):
                print("There is still overlap in the simulation")
                return True
    print("There is no overlap in the simulation")
    return False

def generateRandomSpheres(min_count = 3, max_count = 3, radius = 1, min_loc_range = 5,  max_loc_range = 20.0, collection_name = "SPHERES"):
    
    is_new = 1
 
    if is_new:
        #randomize the size of the bounding box based on the max_loc_range
        max_loc_range = random.uniform(min_loc_range, max_loc_range)
        
        #Create collection if it does not exist already
        target_collection = checkAndCreateCollection(collection_name)
            
        #set random number of spheres
        n_spheres = random.randint(min_count, max_count)
        #print(f"Generating {n_spheres} spheres...")
        
        # Deselect all objects to ensure only the new spheres are selected
        bpy.ops.object.select_all(action='DESELECT')
        
        #create the bounding box
        createBoundingBox(max_loc_range, target_collection)
        bpy.context.view_layer.update() 
        
        #create the spheres and add them to the collection
        createSpheres(max_loc_range, radius, n_spheres, target_collection, collection_name)
        bpy.context.view_layer.update() 
    
 
#########################################################################
    #grab object array
    objs = bpy.data.collections['SPHERES'].objects
    bpy.context.view_layer.update() 
    
    #set diameter for all shperes based on the distance between them
    for base_obj in objs:
        distance_list = []
        if base_obj.name != "Bounding_Box":
            for obj in objs:
                if obj.name != "Bounding_Box":
                    if obj.name !=  base_obj.name:
                        distance = (base_obj.location - obj.location).length
                        distance_list.append(distance)
            
            min_distance = min(distance_list)
            init_size = base_obj.dimensions[0]
            goal_size = min_distance
            factor = goal_size / init_size
            base_obj.scale = (factor, factor, factor)
            bpy.ops.object.select_all(action='DESELECT')
            base_obj.select_set(True)
            bpy.context.view_layer.objects.active = base_obj
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.context.view_layer.update()
      
    for base_obj in objs:
        distance_list = []
        if base_obj.name != "Bounding_Box":
            for obj in objs:
                if obj.name != "Bounding_Box":
                    if obj.name !=  base_obj.name:
                        radii = base_obj.dimensions[0]/2 + obj.dimensions[0]/2 
                        distance = (base_obj.location - obj.location).length - radii
                        distance_list.append(distance)
            
            
            does_touch = False
            for i in distance_list:
                if (i < EPSILON) and  (i > -EPSILON):  # Bedingung: Werte größer 4 entfernen
                    does_touch = True
            
            if (does_touch == False) and distance_list != []:
                new_distance_list = []
                for i in distance_list:
                    if i > EPSILON:
                        new_distance_list.append(i)        
                min_distance = min(new_distance_list)
                init_size = base_obj.dimensions[0]
                goal_size = init_size + 2 * min_distance
                factor = goal_size / init_size
                base_obj.scale = (factor, factor, factor)
                bpy.ops.object.select_all(action='DESELECT')
                base_obj.select_set(True)
                bpy.context.view_layer.objects.active = base_obj
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                bpy.context.view_layer.update()
            
            
    
    """
    #Move objects that are out of bounds inside the bounding box range
    moveOutofBoundsObjects(objs, max_loc_range)
    bpy.context.view_layer.update()
    
    # Use a loop to repeatedly fix and update until the check passes or max iterations hit
    max_fix_iterations = 100
    iteration = 0
    while isSphereOverlap(objs) and iteration < max_fix_iterations:
        fixAllOverlaps(objs)
        bpy.context.view_layer.update()
        iteration += 1
    
    if iteration == max_fix_iterations:
        print(f"Overlap fix failed to converge after {max_fix_iterations} iterations")
 
    #lets check if there is still overlap in the simulation
    isSphereOverlap(objs)
    """
    
    isSphereOverlap(objs)
    
    #add smooth shading to all the objects
    smoothShadeAll(objs)
 
    # Deselect all objepΩcts to ensure only the bounding box is selected (for visual purposes)
    bpy.ops.object.select_all(action='DESELECT')
    
    #Set the bounding box to selected (fot visual purposes)
    bpy.data.collections['SPHERES'].objects['Bounding_Box'].select_set(True)
 
#The main function executes here
generateRandomSpheres(min_count = 5, max_count = 20, min_loc_range = 5,  max_loc_range = 30.0,)