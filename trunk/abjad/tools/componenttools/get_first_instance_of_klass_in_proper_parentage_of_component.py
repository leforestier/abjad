def get_first_instance_of_klass_in_proper_parentage_of_component(component, klass):
   '''.. versionadded:: 1.1.1

   Return first instance of `klass` in parentage of `component`. ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(staff[0], Staff)
      Staff{4}

   Otherwise return ``None``.

   .. versionchanged:: 1.1.2
      renamed ``parenttools.get_first( )`` to
      ``componenttools.get_first_instance_of_klass_in_proper_parentage_of_component( )``.
   '''

   for parent in component.parentage.parentage[1:]:
      if isinstance(parent, klass):
         return parent
