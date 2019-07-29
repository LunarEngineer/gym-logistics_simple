# gym-logistics_simple

The logistics environment is a single agent domain featuring continuous state and discrete action spaces.

## Simple Logistics Environment

In this environment there is a 'road' network created when the environment is created. This network is constructed from a number of nodes and edges of various lengths. One node is always the 'logistics hub' where trucks are 'packed' and 'dispatched' from.

A number of 'customers' travel on the highways surrounding the logistics hub. The customers will always be consuming their resources at various rates and will travel the network at a certain speed.

The distribution hub only has a certain number of trucks available of different types. Different classes of supply may be loaded onto different trucks.

## Running the Environment

This is as simple as using the dockerfile found within this repository. Assuming you have docker installed just build the image and run the container. This will provide you with an image that has Gym and Box2d up and running.