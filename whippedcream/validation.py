from tastypie.validation import FormValidation, CleanedDataFormValidation


class FileFormValidation(FormValidation):
    """
    A validation class that includes files.
    """
    def form_args(self, bundle):
        kwargs = super(FileFormValidation, self).form_args(bundle)
        kwargs['files'] = getattr(bundle, 'files')
        return kwargs


class CleanedDataFileFormValidation(CleanedDataFormValidation):
    """
    A validation class that includes files and returns the form's cleaned_data.
    """
    def form_args(self, bundle):
        kwargs = super(CleanedDataFileFormValidation, self).form_args(bundle)
        kwargs['files'] = getattr(bundle, 'files')
        return kwargs
