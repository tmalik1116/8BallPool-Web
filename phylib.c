#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "phylib.h"

//Allocates memory for new phylib_object with type PHYLIB_STILL_BALL
//Returns pointer to newly created object.
//If malloc fails, return NULL
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){
    //Declare new generic object for still ball
    phylib_object *new_still_ball;

    //Allocate memory and account for failure
    new_still_ball = (phylib_object *) malloc(sizeof(phylib_object));
    if(new_still_ball == NULL){
        return NULL;
    }

    //Passing object type
    new_still_ball->type = PHYLIB_STILL_BALL;

    //Passing object values
    new_still_ball->obj.still_ball.number = number;
    new_still_ball->obj.still_ball.pos = *pos;

    return new_still_ball;
}


//Allocates memory for new phylib_object with type PHYLIB_ROLLING_BALL
//Returns pointer to newly created object.
//If malloc fails, return NULL
phylib_object *phylib_new_rolling_ball( 
    unsigned char number,
    phylib_coord *pos,
    phylib_coord *vel,
    phylib_coord *acc 
){
    phylib_object *new_rolling_ball;

    new_rolling_ball = (phylib_object *) malloc(sizeof(phylib_object));
    if (new_rolling_ball == NULL){
        return NULL;
    }

    new_rolling_ball->type = PHYLIB_ROLLING_BALL;

    new_rolling_ball->obj.rolling_ball.number = number;
    new_rolling_ball->obj.rolling_ball.pos = *pos;
    new_rolling_ball->obj.rolling_ball.vel = *vel;
    new_rolling_ball->obj.rolling_ball.acc = *acc;

    return new_rolling_ball;
}


//Allocates memory for new phylib_object with type PHYLIB_HOLE
//Returns pointer to newly created object.
//If malloc fails, return NULL
phylib_object *phylib_new_hole( phylib_coord *pos ){
    phylib_object *new_hole;

    new_hole = (phylib_object *) malloc(sizeof(phylib_object));
    if (new_hole == NULL){
        return NULL;
    }

    new_hole->type = PHYLIB_HOLE;

    new_hole->obj.hole.pos = *pos;

    return new_hole;
}

//Allocates memory for new phylib_object with type PHYLIB_HCUSHION
//Returns pointer to newly created object.
//If malloc fails, return NULL
phylib_object *phylib_new_hcushion( double y ){
    phylib_object *new_hcushion;

    new_hcushion = malloc(sizeof(phylib_object));
    if (new_hcushion == NULL){
        return NULL;
    }

    new_hcushion->type = PHYLIB_HCUSHION;

    new_hcushion->obj.hcushion.y = y;

    return new_hcushion;
}

//Allocates memory for new phylib_object with type PHYLIB_VCUSHION
//Returns pointer to newly created object.
//If malloc fails, return NULL
phylib_object *phylib_new_vcushion( double x ){
    phylib_object *new_vcushion;

    new_vcushion = (phylib_object *) malloc(sizeof(phylib_object));
    if (new_vcushion == NULL){
        return NULL;
    }

    new_vcushion->type = PHYLIB_VCUSHION;

    new_vcushion->obj.vcushion.x = x;

    return new_vcushion;
}

//Helper function to create new phylib_coord object
phylib_coord *phylib_new_coord(double x, double y){
    phylib_coord *new_coord;

    new_coord = (phylib_coord *) malloc(sizeof(phylib_coord));
    if (new_coord == NULL){
        return NULL;
    }

    new_coord->x = x;
    new_coord->y = y;

    return new_coord;
}

//Allocates memory for new phylib_table object
//Returns pointer to newly created object.
//If malloc fails, return NULL
phylib_table *phylib_new_table(void){

    phylib_table *new_table = (phylib_table *) malloc(sizeof(phylib_table));

    if (new_table == NULL){
        return NULL;
    }

    // initialize all other objects inside of table array

    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    
    phylib_coord *c1 = phylib_new_coord(0.0, 0.0);
    phylib_coord *c2 = phylib_new_coord(0.0, PHYLIB_TABLE_WIDTH);
    phylib_coord *c3 = phylib_new_coord(0.0, PHYLIB_TABLE_LENGTH);
    phylib_coord *c4 = phylib_new_coord(PHYLIB_TABLE_WIDTH, 0.0);
    phylib_coord *c5 = phylib_new_coord(PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH);
    phylib_coord *c6 = phylib_new_coord(PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH);
    new_table->object[4] = phylib_new_hole(c1); //Top Left
    new_table->object[5] = phylib_new_hole(c2); //Middle Left
    new_table->object[6] = phylib_new_hole(c3); //Bottom Left
    new_table->object[7] = phylib_new_hole(c4); //Top Right
    new_table->object[8] = phylib_new_hole(c5); //Middle Right
    new_table->object[9] = phylib_new_hole(c6); //Bottom Right
    
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++){
        new_table->object[i] = NULL;
    }

    free(c1);
    free(c2);
    free(c3);
    free(c4);
    free(c5);
    free(c6);

    new_table->time = 0.0;
    return new_table;
}


//PART 2 UTILITY FUNCTIONS

//Copies the contents of one object to another
void phylib_copy_object(phylib_object **dest, phylib_object **src){
    if(*src == NULL){
        *dest = NULL;
        return;
    }

    phylib_object *new_object;
    new_object = (phylib_object *) malloc(sizeof(phylib_object));

    if (new_object == NULL){
        *dest = NULL;
        return;
    }

    memcpy(new_object, *src, sizeof(phylib_object)); 

    *dest = new_object;
    dest = &new_object; 
}

//Allocates memory for new phylib_table.
//Copies contents from table to new location
phylib_table *phylib_copy_table(phylib_table *table){
    phylib_table *new_table;
    new_table = malloc(sizeof(phylib_table));

    if (new_table == NULL){
        return NULL;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        phylib_copy_object(&new_table->object[i], &table->object[i]);
    }

    new_table->time = table->time;

    return new_table;
}

//Adds object to first empty index of object array
void phylib_add_object(phylib_table *table, phylib_object *object){
    int i = 0;
    while(table->object[i] != NULL){
        i++;
        if (i >= PHYLIB_MAX_OBJECTS){
            return;
        }
    }

    table->object[i] = object;
}

//Frees all non-null pointers in object array
void phylib_free_table(phylib_table *table){
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if (table->object[i] != NULL){
            free(table->object[i]);
        }
    }

    free(table);
}

//Returns difference between two coordinates
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){
    phylib_coord *new_coord;
    new_coord = phylib_new_coord(0.0, 0.0);

    new_coord->x = c1.x - c2.x;
    new_coord->y = c1.y - c2.y;

    phylib_coord c3 = *new_coord;

    free(new_coord);
    return c3;
}

//Returns length of vector c.
double phylib_length(phylib_coord c){
    double length = 0.0;

    length = (c.x * c.x) + (c.y * c.y);

    return (double) sqrt(length);
}

//Returns the dot product of two vectors. 
double phylib_dot_product(phylib_coord a, phylib_coord b){
    //dot product: x*x + y*y
    return (double) ((a.x * b.x) + (a.y * b.y));
}

//returns the distance between 2 phylib_objects
double phylib_distance(phylib_object *obj1, phylib_object *obj2){
    double distance = 0.0;

    if (obj1->type != PHYLIB_ROLLING_BALL){
        return (double) -1;
    }

    if ((obj2 != NULL) && obj2->type == PHYLIB_ROLLING_BALL){ // rolling ball
        distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
    }else if ((obj2 != NULL) && obj2->type == PHYLIB_STILL_BALL){ // still ball
        distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
    }else if ((obj2 != NULL) && obj2->type == PHYLIB_HOLE){ // hole
        distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
    }else if ((obj2 != NULL) && obj2->type == PHYLIB_HCUSHION){ // horizontal cushion
        distance = fabs((obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y)) - PHYLIB_BALL_RADIUS;
    }else if ((obj2 != NULL) && obj2->type == PHYLIB_VCUSHION){ // vertical cushion
        distance = fabs((obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x)) - PHYLIB_BALL_RADIUS;
    }else{
        return (double) -1;
    }
 
    return distance;
}

//PART 3: Physics simulations

// rolls a phylib_rolling_ball based on its velocity and acceleration
void phylib_roll(phylib_object *new, phylib_object *old, double time){
    if ((new != NULL && old != NULL) && (new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL)){
        int isPos = 0;
        int isPosState;


        //updating position of new ball
        //              p                           p1                              v1               t                   a1                      t^2          
        new->obj.rolling_ball.pos.x = (old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + (old->obj.rolling_ball.acc.x * (time * time) / 2.0));

        //              p                           p1                              v1               t                   a1                      t^2          
        new->obj.rolling_ball.pos.y = (old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + (old->obj.rolling_ball.acc.y * (time * time) / 2.0));

        if (phylib_length(new->obj.rolling_ball.vel) >= 0){
            isPos = 1;
        }

        isPosState = isPos;

        //updating velocity of new ball
        //          v                           v1                          a1                         t
        new->obj.rolling_ball.vel.x = (old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time));

        //          v                           v1                          a1                         t
        new->obj.rolling_ball.vel.y = (old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time));

        if (phylib_length(new->obj.rolling_ball.vel) < 0){
            isPos = 0;
        }

        //set velocity and acceleration to 0 if !polarity
        if (isPosState != isPos){
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }

    }
}

unsigned char phylib_stopped(phylib_object *object){
    //check if ball velocity is 0 (below epsilon)
    if (object->type == PHYLIB_ROLLING_BALL && (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON)){
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
        
        return 1;
    }

    return 0;
}

//Handles all types of collisions between objects
void phylib_bounce(phylib_object **a, phylib_object **b){

    phylib_coord *r_ab = phylib_new_coord(0.0, 0.0);
    phylib_coord *v_rel = phylib_new_coord(0.0, 0.0);
    phylib_coord *n = phylib_new_coord(0.0, 0.0);
    double v_rel_n = 0.0;
    double a_speed = 0.0;
    double b_speed = 0.0;

    if (*b != NULL){
    
        switch ((*b)->type){
            case PHYLIB_HCUSHION: // reverse y-vel/acc
                (*a)->obj.rolling_ball.vel.y *= -1.0;
                (*a)->obj.rolling_ball.acc.y *= -1.0;
                break;
            case PHYLIB_VCUSHION: // reverse x-vel/acc
                (*a)->obj.rolling_ball.vel.x *= -1.0;
                (*a)->obj.rolling_ball.acc.x *= -1.0;
                break;
            case PHYLIB_HOLE:
                if (*a != NULL){
                    free(*a);
                    *a = NULL;
                    a = NULL;
                }
                
                break;
            case PHYLIB_STILL_BALL:
                (*b)->type = PHYLIB_ROLLING_BALL;
                (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
                (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
                (*b)->obj.rolling_ball.vel.x = 0.0;
                (*b)->obj.rolling_ball.vel.y = 0.0;
                (*b)->obj.rolling_ball.acc.x = 0.0;
                (*b)->obj.rolling_ball.acc.y = 0.0;
            case PHYLIB_ROLLING_BALL:
                //updating velocities of balls based on physics formulas
                *r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

                *v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

                n->x = (r_ab->x) / phylib_length(*r_ab);
                n->y = (r_ab->y) / phylib_length(*r_ab);

                v_rel_n = phylib_dot_product(*v_rel, *n);

                (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n->x);
                (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n->y);

                (*b)->obj.rolling_ball.vel.x += (v_rel_n * n->x);
                (*b)->obj.rolling_ball.vel.y += (v_rel_n * n->y);

                a_speed = phylib_length((*a)->obj.rolling_ball.vel);
                b_speed = phylib_length((*b)->obj.rolling_ball.vel);

                //set drag for balls a and b
                if (a_speed > PHYLIB_VEL_EPSILON){
                    (*a)->obj.rolling_ball.acc.x = (((-1) * (*a)->obj.rolling_ball.vel.x) / a_speed) * PHYLIB_DRAG;
                    (*a)->obj.rolling_ball.acc.y = (((-1) * (*a)->obj.rolling_ball.vel.y) / a_speed) * PHYLIB_DRAG;
                }

                if (b_speed  > PHYLIB_VEL_EPSILON){
                    (*b)->obj.rolling_ball.acc.x = (((-1) * (*b)->obj.rolling_ball.vel.x) / b_speed) * PHYLIB_DRAG;
                    (*b)->obj.rolling_ball.acc.y = (((-1) * (*b)->obj.rolling_ball.vel.y) / b_speed) * PHYLIB_DRAG;
                }
                break;
            default:
                break;
        }
    }
    free(r_ab);
    free(v_rel);
    free(n);
}

//Returns the number of ROLLING_BALLs on the table
unsigned char phylib_rolling(phylib_table *t){
    unsigned char balls = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            balls++;
        }
    }

    return balls;
}


//Simulates a segment of a turn, returns updated table
phylib_table *phylib_segment(phylib_table *table){

    if (phylib_rolling(table) == 0){
        return NULL;
    }

    phylib_table *new_table = phylib_copy_table(table);
    double outsideTime = new_table->time;

    //outer loop to go from PHYLIB_SIM_RATE to PHYLIB_MAX_TIME
    //copy the table (before returning) copy table time = current table + the current time
    for (double time  = PHYLIB_SIM_RATE; time < PHYLIB_MAX_TIME; time += PHYLIB_SIM_RATE){
        //loop through objects to apply roll
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL){
                phylib_roll(new_table->object[i], table->object[i], (time));
            }
        }

        //re-loop through objects to check for collisions
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            //new_table->time += PHYLIB_SIM_RATE;
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL){
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++){

                    //loop for checking if ball has collided with another object
                    if (j != i && ((phylib_distance(new_table->object[i], new_table->object[j])) < 0.0)/* && (phylib_distance(new_table->object[i], new_table->object[j]) != (-1.0))*/){
                        
                        // account for distance returning -1.0 as error code
                        if (phylib_distance(new_table->object[i], new_table->object[j]) != -1.0){
                            phylib_bounce(&new_table->object[i], &new_table->object[j]);
                            new_table->time += time;
                            return new_table;
                        }
                    }
                }

                if (phylib_stopped(new_table->object[i])){ // case where ball stops rolling
                    new_table->time += time;
                    return new_table;
                }
            }
        }
    }
    new_table->time += outsideTime;
    return new_table;
}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        sprintf( string, "NULL;" );
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        sprintf( string,
        "STILL_BALL (%d,%6.1lf,%6.1lf)",
        object->obj.still_ball.number,
        object->obj.still_ball.pos.x,
        object->obj.still_ball.pos.y );
        break;
    case PHYLIB_ROLLING_BALL:
        sprintf( string,
        "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
        object->obj.rolling_ball.number,
        object->obj.rolling_ball.pos.x,
        object->obj.rolling_ball.pos.y,
        object->obj.rolling_ball.vel.x,
        object->obj.rolling_ball.vel.y,
        object->obj.rolling_ball.acc.x,
        object->obj.rolling_ball.acc.y );
    break;
    case PHYLIB_HOLE:
        sprintf( string,
        "HOLE (%6.1lf,%6.1lf)",
        object->obj.hole.pos.x,
        object->obj.hole.pos.y );
        break;
    case PHYLIB_HCUSHION:
        sprintf( string,
        "HCUSHION (%6.1lf)",
        object->obj.hcushion.y );
        break;
    case PHYLIB_VCUSHION:
        sprintf( string,
        "VCUSHION (%6.1lf)",
        object->obj.vcushion.x );
        break;
    }
    return string;
}
