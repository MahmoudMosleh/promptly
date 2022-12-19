from support_functions import answer_column_process, is_assessment_fully_completed_column_process

source_columns_mapping= {	
"birthdate": {"type":"datetime", "error":"coerce"},
"completed_at":  {"type":"datetime", "error":"coerce"},
"created_at":  {"type":"datetime", "error":"coerce"},
"updated_at":  {"type":"datetime", "error":"coerce"},
"event_date": {"type":"datetime", "error":"coerce"},
"assessment_id": {"type":"Int64"},
"patient_id": {"type":"Int64"},
"event_id": {"type":"Int64"},
"institution": {"type":"Int64"},
"answers": {"type": "func", "process": answer_column_process},
"is_assessment_fully_completed": {"type": "func", "process": is_assessment_fully_completed_column_process},
}
