import logging

from galaxy import (
    exceptions,
    model,
    util
)

log = logging.getLogger(__name__)


class JobPortsView(object):

    def __init__(self, app):
        self._app = app

    def register_container_information(self, job_id, **kwd):
        job = self.__authorize_job_access(job_id, **kwd)
        container_runtime = kwd.get("container_runtime")
        log.info(kwd)
        self._app.interactivetool_manager.configure_entry_points(job, container_runtime)
        return {"message": "ok"}

    # Copy/paste from JobFilesView - TODO: de-duplicate.
    def __authorize_job_access(self, encoded_job_id, **kwargs):
        key = "job_key"
        if key not in kwargs:
            error_message = "Job files action requires a valid '%s'." % key
            raise exceptions.ObjectAttributeMissingException(error_message)

        job_id = self._security.decode_id(encoded_job_id)
        job_key = self._security.encode_id(job_id, kind="jobs_files")
        if not util.safe_str_cmp(kwargs["job_key"], job_key):
            raise exceptions.ItemAccessibilityException("Invalid job_key supplied.")

        # Verify job is active. Don't update the contents of complete jobs.
        sa_session = self._app.model.context.current
        job = sa_session.query(model.Job).get(job_id)
        if job.finished:
            error_message = "Attempting to read or modify the files of a job that has already completed."
            raise exceptions.ItemAccessibilityException(error_message)
        return job

    @property
    def _security(self):
        return self._app.security
