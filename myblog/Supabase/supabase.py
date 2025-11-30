from supabase import create_client
from django.conf import settings


supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_to_cloud(file):
    file_name = file.name

    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        file= file.read(),
        path=file_name
    )

    return supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_name)