FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY github_archive ${LAMBDA_TASK_ROOT}/github_archive
COPY requirements.txt  ${LAMBDA_TASK_ROOT}/requirements.txt

# Install the function's dependencies using file requirements.txt
RUN  python3 -m pip install -r requirements.txt

ENV PYTHONPATH=github_archive

# Set the CMD to your handler
CMD [ "github_archive.lambda_handler" ]
