def get_notes_JSON(note):
        note_list = {
                'subject': note.subject,
                'description': note.description,
                'label': note.label.label,
                'color': note.label.color,
                }
        return {'note': note_list}