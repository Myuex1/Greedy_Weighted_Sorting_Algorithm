"""
Copyright (c) 2026 Elijah W
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

## Start Databases


Weights = {                                                                    # Stores the component weights (this is what gets adjusted to tune the model)

    ## Components (can be chemicals or whatever you want to consider)
        
        "comp_1" : {"Weight":1},                                               # Weight of components 1-10 (parts of a recipe)
        "comp_2" : {"Weight":1},                                               
        "comp_3" : {"Weight":1},                                               
        "comp_4" : {"Weight":1},                                               
        "comp_5" : {"Weight":1},                                               
        "comp_6" : {"Weight":1},                                               
        "comp_7" : {"Weight":1},                                               
        "comp_8" : {"Weight":1},                                               
        "comp_9" : {"Weight":1},                                              
        "comp_10" : {"Weight":1},                                              
        
    ## Physical Properties
        
        "Density": {"Weight":1},                                               # Weight of density
        "Height": {"Weight":10000,}                                            # Weight of height (example of a most important factor) (if heights are same, considers other factors, but height will dominate if set to 10000)

}


Products = {                                                                   # Product database

        "Product_A":
            {
            
            "Density": 4,                                                      # Intensive property (constant for all variants)
            
            "Variants": ["V1","V2","V3"],                                      # Physical (unique to each variant)
            "Height": [10, 15, 20],
            "Scalar": [6, 5, 4],                                               # Scalar * Component = Flow Rate (if no scalar = 1)
            
            "Recipe":{                                                         # Chemical/Ingredients (same regardless of variant)(parts of a recipe)
                "comp_1": 85,
                "comp_2": 45,
                "comp_3": 0,
                "comp_4": 0,
                "comp_5": 45,
                "comp_6": 0,
                "comp_7": 65,
                "comp_8": 0,
                "comp_9": 0,
                "comp_10": 0,
            },
        },
        
        "Product_B":
            {
            
            "Density": 2,                                                     
            
            "Variants": ["V1","V2","V3"],                                      
            "Height": [20, 15, 30],
            "Scalar": [2, 4, 3],
            
            "Recipe":{                                                       
                "comp_1": 90,
                "comp_2": 15,
                "comp_3": 0,
                "comp_4": 90,
                "comp_5": 0,
                "comp_6": 35,
                "comp_7": 0,
                "comp_8": 0,
                "comp_9": 0,
                "comp_10": 0,
            },
        },
        
        "Product_C":
            {
                                                                               
            "Density": 1,
                                                                            
            "Variants": ["V1","V2","V3"],
            "Height": [55, 45, 40],
            "Scalar": [3, 4, 2],
            
            "Recipe":{                                                       
                "comp_1": 100,
                "comp_2": 30,
                "comp_3": 0,
                "comp_4": 0,
                "comp_5": 60,
                "comp_6": 0,
                "comp_7": 20,
                "comp_8": 0,
                "comp_9": 0,
                "comp_10": 0,
            }
        },
        
        "Product_D":
            {
                                                                              
            "Density": 3,
                                                                              
            "Variants": ["V1","V2","V3"],
            "Height": [55, 35, 20],
            "Scalar": [1, 3, 2],
            
            "Recipe":{                                                        
                "comp_1": 70,
                "comp_2": 30,
                "comp_3": 0,
                "comp_4": 0,
                "comp_5": 50,
                "comp_6": 0,
                "comp_7": 20,
                "comp_8": 0,
                "comp_9": 0,
                "comp_10": 0,
            }
        },
        
        "Product_E":
            {
                                                                              
            "Density": 1.5,
                                                                               
            "Variants": ["V1","V2","V3"],
            "Height": [20, 25, 30],
            "Scalar": [4, 2, 3],
            
            "Recipe":{                                                        
                "comp_1": 95,
                "comp_2": 50,
                "comp_3": 0,
                "comp_4": 0,
                "comp_5": 0,
                "comp_6": 40,
                "comp_7": 0,
                "comp_8": 0,
                "comp_9": 0,
                "comp_10": 0,
            }
        },
}


## End Databases    
 


## Start Variables   


weight_array = [0] * 12                                                        # Stores all weights 
to_do_schedule = [""] * 20                                                     # Stores the pre organized schedule 
daily_product  =[None] * 20                                                    # Stores the name for the split function 
daily_variant = [None] * 20                                                    # Stores the SKU for the split function
product_remaining = [None] * 20                                                # Holds the updated list as the algorithm is running through "to_do_schedule" 
variant_remaining = [None] * 20                                                # Same thing but for SKU/variant

working_scalar_A = 0                                                           # Stores scalar for A 
working_scalar_B = 0                                                           # Stores scalar for B 


                                                # Physical


working_density_A = 0                                                          # Stores density data for A 
working_density_B = 0                                                          # Stores density data for B

density_diff = 0                                                               # Stores diff in density

working_height_A = 0                                                           # Stores height data for A
working_height_B = 0                                                           # Stores height data for B

height_diff = 0                                                                # Stores diff in height


                                                # Chemical


working_A_product = [0] * 10                                                   # Parts from database
working_B_product = [0] * 10

Flow_A = [0] * 10                                                              # Flow rate (parts * scalar)
Flow_B = [0] * 10

recipe_diff = [0] * 10                                                         # Difference in flow rates


                                                # Other
                                                                         
                                                                         
scores = [0] * 10                                                              # Stores individual component scores

height_score = 0                                                               # Amount height contributed to final score
density_score = 0                                                              # Amount density contributed to final score
final_score = 0                                                               
best_score = 1000000000                                                        # Stores the best score, updated when a decision is made, starts as a big number so anything is smaller
      
final_schedule = []                                                            # Place where the final schedule is populated into

exit_loop=0                                                                    # Used to exit a loop


                                                                  # Manipulated


starter_product = "Product_A"                                                  # Set starting point for algorithm
starter_variant = "V1"
current_product_A = starter_product                                            # Set current A name to starter option
working_variant_A = starter_variant                                            # The number of the variant (order) in the array "to_do_schedule"
current_variant_A = starter_variant                                            # The name of the variant in the array "to_do_schedule"

A = 0                                                                          # "A" is the number slot we are comparing all of B products to
      

## End Variables



## Start Program


for component in Weights:                                                      # Loops component weight array and populates array from database

        weight_array[exit_loop] = Weights[component]["Weight"]
        exit_loop = exit_loop + 1


to_do_schedule = [                                                             # Hard coded array that holds the pre-optimized schedule (redesign to import this)

"Product_A-V1",
"Product_A-V2",
"Product_C-V2",
"Product_B-V2",
"Product_D-V1",
"Product_E-V1",
"Product_C-V3",

]


final_schedule.append(starter_product + "-" + starter_variant)                 # Adds starter product as slot one in final schedule
to_do_schedule.remove(starter_product + "-" + starter_variant)                 # Removes starter product from to do schedule

num_items = len(to_do_schedule)                                                # Sets "num_item" to the length of the list of "to_do_schedule"


for n in range (num_items):                                                    # Splits the name into product and Variant

        if '-' in to_do_schedule[n]:                                           # If there is a - in "to_do_sch"
                temp_hold_product = to_do_schedule[n].split('-')                   # Split name into 2 parts around "-" 
                daily_product[n] = temp_hold_product[0]                            # Store name in "temp_hold_product[0]"
                daily_variant[n] = temp_hold_product[1]                            # Store SKU in  "temp_hold_product[1]"



## Start Main Loop



print("")
print("============================================================")
print("                   STARTING OPTIMIZATION...  ")


while len(to_do_schedule) > 0:                                                 # While there are still things to compare

    best_score = 1000000000                                                    # Clear ram
    best_index = 0                                                             # Clear ram
    best_score_slot = ""                                                       # Clear ram

    working_density_A = Products[current_product_A]["Density"]                 # Sets ram for A values 
    working_variant_A = Products[current_product_A]["Variants"].index(current_variant_A) # "" 
    working_A_product = list(Products[current_product_A]["Recipe"].values())    # ""     
    working_scalar_A = Products[current_product_A]["Scalar"][working_variant_A] # ""       
    working_height_A = Products[current_product_A]["Height"][working_variant_A] # ""
    
    print("============================================================")            
    print(f"Finding best match for: {current_product_A}-{current_variant_A}")
    print("")
    
    for B in range(len(to_do_schedule)):                                       # For each one until 0 left
    
        if daily_product[B] is None or daily_variant[B] is None:                   # Breaks loop if none left
            continue       
        
        current_product_B = daily_product[B]                                       # Sets ram to B data
        current_variant_B = daily_variant[B]                                       # ""
        working_density_B = Products[current_product_B]["Density"]                 # ""
        working_variant_B = Products[current_product_B]["Variants"].index(daily_variant[B]) # ""                                                     
        working_B_product = list(Products[current_product_B]["Recipe"].values())    # "" 
        working_scalar_B = Products[current_product_B]["Scalar"][working_variant_B] # ""
        working_height_B = Products[current_product_B]["Height"][working_variant_B] # ""
             
        
                                    # Chemical Parts   
                                    
                                    
        for f in range (10):                                                   # For all 10 components:
            
            Flow_A[f] = working_A_product[f] * working_scalar_A                    # Take parts and multiply by scalar for A
            Flow_B[f] = working_B_product[f] * working_scalar_B                    # "" for B
            
            recipe_diff[f] = abs(Flow_A[f] - Flow_B[f])                            # Subtract one from other
            
            scores[f] = recipe_diff[f] * weight_array[f]                           # Multiply difference by the weight 
        
           
                                    # Height Part
               
                
        height_diff = abs(Products[current_product_A]["Height"][working_variant_A] 
                        - Products[current_product_B]["Height"][working_variant_B])
                        
        height_score = height_diff * weight_array[11]
        

                                    # Density Part
                                    
                                    
        density_diff = abs(Products[current_product_A]["Density"] -
                          Products[current_product_B]["Density"])
                        
        density_score = density_diff * weight_array[10]
        
        
                                   # Add All "Scores"
                                    
                                   
        final_score = sum(scores)                                              # Sums chemical score array
        final_score = final_score + height_score + density_score
        
             
        if final_score < best_score:                                           # If current score is better than best score
            best_score = final_score                                             # Set best score to current score
            best_index = B                                                       # Store variant slot
            best_score_slot = to_do_schedule[B]                                  # Store slot number as best index
            
            print(f"  [X] Checking {to_do_schedule[B]}..... Score: {final_score:.0f} <-- NEW BEST")
        
        else:
            print(f"  [ ] Checking {to_do_schedule[B]}..... Score: {final_score:.0f}")

            
    scheduled_product = to_do_schedule[best_index]                             # Stores best product
    final_schedule.append(scheduled_product)                                   # Adds best product to final schedule
    to_do_schedule.pop(best_index)                                             # Removes choice from to do schedule
    daily_product.pop(best_index)                                              # Removes choice product from the daily product list
    daily_variant.pop(best_index)                                              # Removes variant from the variant daily list
   
    temp_split = scheduled_product.split('-')                                  # Splits the best product into its name and SKU
    current_product_A = temp_split[0]                                          # Sets A to the best match found to start the loop again
    current_variant_A = temp_split[1]                                          # "" SKU
    
    print("")
    print(f"       >>> BEST FOUND: {best_score_slot} | Score: {best_score:.0f}<<<")
    print("")
    
    
    
## End Main Loop  
  


print("============================================================")    
print("")       
print("         ======================================")
print("         *      FINAL OPTIMIZED SCHEDULE      *")
print("         *      ------------------------      *")

for i, order in enumerate (final_schedule):
        print(f"         *          {i+1}: {order}           *") 
print("         ======================================")
print("")
print("============================================================")







print("")
print ("By: Elijah Whiting :)")


## End Program
