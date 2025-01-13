show image repositories;
show images in image repository test.public.repo;

desc compute pool cpu1;

show services;
alter service test.public.service1 resume;
show endpoints in service test.public.service1;
show service instances in service test.public.service1;
show service containers in service test.public.service1;
show roles in service test.public.service1;

alter service test.public.service1 suspend;
alter compute pool cpu1 suspend;
show compute pools;
