# Django-RQ

## Description:
Django-RQ is library that combines Django with RQ(Redis Queue) that allows for the configuration of queues (to run jobs) within Django's `settings.py`. This document goes over some useful commands and how to write custom jobs and using the scheduler.

## Documentation:
For more details on Django-RQ, please refer to the [official project repo](https://github.com/rq/django-rq).

## Commands:

Note: These commands assume the use of the `default` queue defined in `settings.py`.

* `rqworker`: Starts a worker for every queue specified as arguments.

    * Example: `docker compose exec api python manage.py rqworker default`.

* `rqscheduler`: Starts the built-in scheduler:

    * Example: `docker compose exec api python manage.py rqscheduler`.

* `rqstats`: Displays statistics of the scheduled jobs from the RQ built-in scheduler.

    * Example: `docker compose exec api python manage.py rqstats`.
    * Example: `docker compose exec api python manage.py rqstats --json ## Output as JSON`.


## Writing Custom Jobs:

* When writing custom jobs, you need to use the `@job` decortator provided from the `django-rq` library.

    * Example:
        ```
        from django-rq import job

        @job("default")
        def some_job_func():
            pass    
        ```

## Using the Scheduler:

* You can retrieve the `django-rq` scheduler in order to queue new jobs. After, you can queue a new job by using either the `enqueue_at` or the `enqueue_in` method from the scheduler.

    * Example:
    ```
    import django-rq
    from datetime import timedelta    
    scheduler = django_rq.get_scheduler("default")
    job = scheduler.enqueue_in(timedelta(min=1), some_job_func)
    ```
* If you wish to see the current jobs in the scheduler queue, you can use the scheduler's `.get_jobs()` method.

    * Example: 
    ```
    from django_rq
    scheduler = django_rq.get_scheduler("default")
    for job in scheduler.get_jobs():
        print(job)        
    ```
    * Note: To delete a job from the scheduler queue, you can use the `.delete()` method belonging to a job. 
        * Example: 
        ```
        for job in scheduler.get_jobs():
            job.delete()
        ```











 
