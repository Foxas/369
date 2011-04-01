ALTER TABLE web369_scrappeddocument ENGINE=MyISAM;
ALTER TABLE web369_scrappeddocument
    CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE web369_scrappeddocument 
    ADD FULLTEXT(content_ascii, subject_title_ascii);
