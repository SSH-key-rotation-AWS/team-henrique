from pathlib import Path
from argparse import ArgumentParser, ArgumentError
from switcheroo.ssh.scripts.custom_argument_exceptions import (
    InvalidArgumentError,
    MissingArgumentError,
)
from switcheroo.ssh.data_org.publisher import KeyPublisher, FileKeyPublisher
from switcheroo.ssh.data_org.publisher.s3 import S3KeyPublisher
from switcheroo import paths
from switcheroo.ssh import MetricConstants
from metric_system.functions.metric_publisher import MetricPublisher
from metric_system.functions.aws_metric_publisher import AwsMetricPublisher
from metric_system.functions.file_metric_publisher import FileMetricPublisher


def create_argument_parser() -> ArgumentParser:
    # pylint: disable=R0801
    argument_parser = ArgumentParser(
        prog="switcheroo_publish",
        description="Creates public/private SSH keys and publishes "
        + "the public key either locally or to S3 (default is S3)",
        epilog="Thanks for using switcheroo_publish! :)",
    )
    argument_parser.add_argument(
        "hostname",
        help="the hostname of the server",
    )
    argument_parser.add_argument(
        "user",
        help="the username of the connecting client",
    )
    argument_parser.add_argument(
        "-ds",
        "--datastore",
        default="s3",
        choices=["s3", "local"],
        required=False,
        help="choose where to store the public key,\
            on S3 or on the local system (default is S3)",
    )
    argument_parser.add_argument(
        "--bucket",
        required=False,
        help="If s3 is selected, the bucket name to store the key in",
    )
    argument_parser.add_argument(
        "--sshdir",
        default=paths.local_ssh_home(),
        required=False,
        help="The absolute path to\
            the directory that stores local keys (ie /home/you/.ssh)",
    )
    argument_parser.add_argument(
        "-m",
        "--metric",
        choices=["file", "aws"],
        required=False,
        help="opt to have metrics published, either to AWS cloudwatch\
            or to the local file system",
    )
    argument_parser.add_argument(
        "--metricpath",
        default=paths.local_metrics_dir(),
        required=False,
        help="The absolute path to the directory\
            that stores the metrics (if metrics are stored locally)",
    )

    return argument_parser


def _local_store(sshdir: str, bucket: str | None = None) -> FileKeyPublisher:
    if bucket is not None:
        raise InvalidArgumentError(
            'Invalid argument "--bucket" when storing the keys locally'
        )
    return FileKeyPublisher(Path(sshdir))


def _s3_store(sshdir: str, bucket: str | None = None) -> S3KeyPublisher:
    if bucket is None:
        raise MissingArgumentError("The s3 option requires a bucket name!")
    return S3KeyPublisher(bucket, root_ssh_dir=Path(sshdir))


def _metrics(
    metricpath: str | None = None, metric: str | None = None
) -> MetricPublisher:
    if metric == "file":  # publish to file system
        return FileMetricPublisher(Path(metricpath))
    if metric == "aws":  # publish to cloudwatch
        if metricpath is not None:
            raise InvalidArgumentError(
                'Invalid argument "--metricpath" when storing the metrics on AWS'
            )
        return AwsMetricPublisher(MetricConstants.NAME_SPACE)
    raise MissingArgumentError(
        'Please specify either "file" or "aws" after the -m/--metric option.'
    )


def main():
    parser = create_argument_parser()
    try:
        args = parser.parse_args()
    except ArgumentError as error:
        raise InvalidArgumentError(f"Invalid argument: {error}") from error
    key_publisher: KeyPublisher | None = None
    metric_publisher: MetricPublisher | None = None
    if args.datastore == "local":  # If the user chose to store the public key locally
        key_publisher = _local_store(args.sshdir, args.bucket)
    else:  # If the user chose to store the public key on S3 or chose to default to S3
        key_publisher = _s3_store(args.sshdir, args.bucket)
    if args.metric:  # If the user chose to publish metrics
        metric_publisher = _metrics(args.metricpath, args.metric)
    assert key_publisher is not None
    key_publisher.publish_key(
        args.hostname, args.user, metric_publisher=metric_publisher
    )


if __name__ == "__main__":
    main()
