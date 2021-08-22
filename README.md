## Sewing Pattern Library

The Sewing Pattern Library helps users to keep track of the sewing patterns they own. Registered users can search for the patterns in the database, and they can add new patterns to the database if the sewing pattern is not already there. Users can leave reviews of patterns. They can also add patterns to their personal library and delete patterns from their personal library.

In the future users will be able search their personal libraries. Users will be able add notes to the patterns in their personal library, these notes will not be visible to other users.

Test the app on [Heroku](https://sewing-pattern-library.herokuapp.com/).

Current test data for patterns include patterns named B6354, B6414, 6808, Moneta, Coco, and Arielle and pattern companies include Butterick, Tilly and the Buttons, Mekkotehdas, New Look. You can search for partial names. Please note that the pattern name needs to be unique when adding new patterns to the database.

### Current features:

- user registration
- login and logout
- search for pattern by name or code, company, fabric type or a combination of these
- add a pattern to the database
- add a public review to a pattern
- individual pattern pages that show pattern information and reviews
- personal pattern library page
- save & delete patterns from your personal library

### Things to add & update:

- look & feel of the app: bootstrap
- clarity to error messages
- add pre-populated forms when something goes wrong with suitable error messages
- security: csrf-tokens
- change individual pattern page identifier from name to id
- fix garment type display on individual pattern page (commas missing)
- pattern search by garment type

### Future features:

- edit & delete reviews
- add personal notes to patterns in your library
- search personal pattern library
