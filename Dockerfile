ARG PYTHON_VERSION=3.8
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

LABEL author="Ben Fortuna <fortuna@micronode.com>"

COPY *.py ${LAMBDA_TASK_ROOT}
COPY package/python/* ${LAMBDA_TASK_ROOT}/package/python/

CMD ["app.handler"]
