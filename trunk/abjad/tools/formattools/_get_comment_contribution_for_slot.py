def _get_comment_contribution_for_slot(component, slot):
   '''.. versionadded:: 1.1.2
   '''
   from abjad.tools import marktools

   result = [ ]
   comment_marks = marktools.get_all_comment_marks_attached_to_component(component)
   for comment_mark in comment_marks:
      if comment_mark._format_slot == slot:
         result.append(comment_mark.format)
   return result
