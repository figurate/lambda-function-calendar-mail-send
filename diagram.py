from diagrams import Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.engagement import SES
from diagrams.aws.integration import SNS

with Diagram("Calendar Mail Send", show=False, direction="TB"):

    topic = SNS("calendar topic")
    ses = SES("simple email service")

    topic >> Edge(label="published calendar") >> Lambda("calendar mail send") >> Edge(label="multipart email") >> ses
