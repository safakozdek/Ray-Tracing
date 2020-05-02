# Ray-Tracing
Ray tracing is a rendering technique for generating an image by tracing the path of light as pixels in an image plane and simulating the effects of its encounters with virtual objects.

## How to run?

### Input.txt format:
**[Number of spheres]** \
*For each sphere:*
* **[colorR, colorG, colorB]** → Comma seperated RGB values 
* **[centerX, centerY, centerZ]** → Comma seperated center coordinates 
* **[radius]** 
* **[diffuse Coefficient]** 
* **[reflection Coefficient]** 

**[Number of planes]**\
*For each plane:*
* **[colorR, colorG, colorB]** → Comma seperated RGB values
* **[centerX, centerY, centerZ]** → Comma seperated point coordinates 
* **[normalX, normalY, normalZ]** → Comma seperated normal vector 
* **[diffuse Coefficient]**
* **[reflection Coefficient]** 


You can check example [input.txt](https://github.com/safakozdek/Ray-Tracing/blob/master/input.txt)
### Run:
You need an environment that has python3 with numpy and pillow libraries installed. Then follow the steps:
* Modify input.txt which is located in the same directory with ray_tracer.py
* Use `python ray_tracer.py` to run the script. 
* Output.png or output.jpeg will be generated.\

PS: It takes a few minutes to generate the output. Please be patient.
