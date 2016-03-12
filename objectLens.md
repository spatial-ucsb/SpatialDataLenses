###Baltimore City Vacants

This dataset is an online repository of vacant building and lot features across Baltimore City. Updated monthly, the dataset keeps track of parcel properties that are not currently on the market, and are no longer occupied or condemned. Each feature contains attributes for several parent administrative jurisdictions including block lot, full address, neighborhood, and city council and police districts. In addition, each feature has a values for a coordinate location and a notice date generated upon initial inspection. Available on Baltimore’s web portal OpenBaltimore, this public dataset can be used via online mapping tools, or downloaded in tabular form for an array of projects. As suggested by OpenBaltimore administer Mayor’s Office of Information Technology (MOIT), this dataset is intended to promote open government, but does not yet have explicit typical uses. To date, there are no known geographic studies with this data. However, for economic and social scientists, this data could be useful when looking at urban growth dynamics.


Based on the coordinates attribute, one could discretely plot where vacant growth proximity and clustering occurs. To investigate this, I propose the CoreConcepts object lens to answer the questions:
>*where do we find vacant clustering?*

>*how do these clusters relate to administrative district boundaries?* 

Looking through the object lens, an economist or city planner could conduct proximity analysis between each vacant data point and to their respective administrative bounding boxes. This valuable information could influence policy, including suggesting where to focus and deviate rehabilitation spending.

###Preprocesing

The user supplies tabular data with a predetermined location attribute (longitude & latitude). Once calling the CoreConcepts object constructor, the following settings will be initialized:
>

Through the object lens, many simple distance questions can be asked such as, how close is a given parcel to the center or edge of its neighborhood? What is a parcel’s nearest neighbors? Are adjacent parcels also vacant?
What pre-processing do you have to apply to your data set so that it can answer the questions? (e.g., how can you construct the links in a network, this defines the constructors)
Preprocessing of this data would only include joining the provided points to their respective area parcels via latitude/longitude data. To construct the ‘service areas’ associated with administrative districts could be a simple joining of the two areas.
Can you implement this preprocessing? If possible, try it out (for example, with a Python script or Java script or ArcGIS command etc.)

What secondary lens would make sense to apply to the data? Maybe another content lens or a quality lens? Which? What would that require (along the same lines as for the primary lens, but just sketched).
The CoreConcepts field lense would also provide valuable insight, potentially aggregating information in some regions and interpolating in others, providing a continuous ‘heat map’ to better study density of housing decay. This would require fitting the lat/lon information to a grid, picking a cell size, and assigning binary results to each pixel (‘is vacant’, ‘is not vacant’).


http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html