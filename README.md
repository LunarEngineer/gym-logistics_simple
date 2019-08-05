# gym-logistics_simple

The logistics environment is a single agent domain featuring continuous state and discrete action spaces.

## Simple Logistics Environment

In this environment there is a 'road' network created when the environment is created. This network is constructed from a number of nodes and edges of various lengths. One node is always the 'logistics hub' where trucks are 'packed' and 'dispatched' from.

A number of 'customers' travel on the highways surrounding the logistics hub. The customers will always be consuming their resources at various rates and will travel the network at a fixed speed.

The distribution hub only has a certain number of trucks available of different types. Different classes of supply may be loaded onto different trucks.

## Action Space

The action space in this environment is an $n x m + 1$ unsigned uint8 matrix where n is the number of trucks and m is the number of supply classes in the problem. When passing actions the first element of each row is inerpreted as the 'customer number' that truck should seek. The remaining m elements in that row will be interpreted as the supply priority for that truck; this can be used to prioritize supplies of certain classes when that truck fills at the depot.

Customer numbers can be in the range (0,inf) and the environment interprets any customer number between 0 and one less than the number of customers (0,n-1) as the customer to dispatch. Passing a value equal to the number of customers will tell that truck to return to the depot to restock, and passing anything greater than n results in that truck not moving. Trucks path directly towards customers using a variant of Dijkstras.

## State Space

Every step in the environment the state is characterized by a (n_1+n_2 x m + 2) matrix where n_1 is the number of customers, n_2 the number of trucks and m the number of supply classes.

The first two columns are the x,y coordinates of the customers / trucks while the remaining m columns are the quantity of supply in that customer / truck.

## Running the Environment

After installation create a new environment with

```{python}
env = gym.make('gym_logistics_simple:logistics-simple-v0')
```