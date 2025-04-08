CREATE DATABASE [$(AXIS_DATABASE_NAME)]
GO

USE [$(AXIS_DATABASE_NAME)];
GO

CREATE TABLE program (
    id INT NOT NULL IDENTITY,
    pa_number VARCHAR(1028) NOT NULL,
    program_name VARCHAR(1028) NOT NULL,
    segment VARCHAR(1028) NOT NULL,
    sector VARCHAR(1028) NOT NULL,
    division VARCHAR(1028) NOT NULL,
    tier INT,
    contract_value BIGINT NOT NULL,
    active_status BIT NOT NULL,
    PRIMARY KEY (id)
);
GO

INSERT INTO [program] (pa_number, program_name, segment, sector, division, tier, contract_value, active_status)
VALUES 
('1PHLMV', 'Quo Vadis', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 2, 31415629467, 1),
('1DVH8T', 'Painted Lady', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 83233449721, 1),
('1FAGGW', 'Why Has Bodhi-Dharma Left for the East?: A Zen Fable', 'SAS', 'Space Systems', 'Surveillance Systems', 2, 36353475629, 0),
('19MSTR', 'Emperor Waltz, The', 'SAS', 'Space Systems', 'Surveillance Systems', 2, 89919689752, 1),
('1K6BHP', 'Innocent Blood', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 15086029062, 1),
('1LF37L', 'House of Angels', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 2, 17058313872, 1),
('1DUMVC', 'Red Dawn', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 58931283490, 1),
('19OXB6', 'Snow Dogs', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 13866035610, 1),
('1H3EZJ', 'Boys on the Side', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 3, 68219679290, 1),
('1QJYDE', 'Boogeyman', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 16509455949, 1),
('1AOXVN', 'So Proudly We Hail!', 'SAS', 'Space Systems', 'Spectral Solutions', 4, 8112327131, 1),
('1GLKRQ', 'That Darn Cat!', 'SAS', 'Space Systems', 'Spectral Solutions', 1, 38652687145, 1),
('1BSDOZ', 'Puss in Boots', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 3252030265, 1),
('1NQMHN', 'High Cost of Living, The', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 33625325875, 0),
('1M2NX2', 'Lilo & Stitch', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 20481866256, 0),
('171UBT', 'Rammbock', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 81027154087, 0),
('1KBUTC', 'Journey to the West: Conquering the Demons', 'SAS', 'Intelligence & Cyber', 'I&C International', 4, 81055210605, 1),
('12GMTV', "Li'l Abner", 'SAS', 'Intelligence & Cyber', 'I&C International', 1, 90852477864, 0),
('16NQZX', 'Piece of the Action, A', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 45323906089, 1),
('1KVLSH', "Emperor's Naked Army Marches On, The", 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 2, 10726575487, 0),
('1FGEDU', 'Terror, The', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 33812880158, 1),
('1NJEHC', 'Corto Maltese: Ballad of the Salt Sea', 'SAS', 'Intelligence & Cyber', 'I&C International', 2, 2030023640, 1),
('16NEWS', 'Pleasure Party', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 86957852141, 1),
('1EBGMK', 'Middle of Nowhere', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 88668842695, 0),
('1H6YX2', 'Scream 4', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 10725446581, 1),
('198W8H', "Rally 'Round the Flag, Boys!", 'SAS', 'Intelligence & Cyber', 'I&C International', 1, 16975340832, 1),
('17VYPD', 'Bend of the River', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 12535401324, 1),
('1FB8JE', 'Quick and the Dead, The', 'SAS', 'Maritime', 'Sonar & Command Systems', 2, 14087001047, 0),
('197DTK', 'New World, The', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 10379047809, 1),
('1MYYSX', 'Junebug', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 3, 11400812145, 1),
('1M1BCG', 'Land of the Pharaohs', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 4, 12346314307, 1),
('16BS1F', 'The Conrad Boys', 'SAS', 'Maritime', 'Sonar & Command Systems', 4, 16490706138, 1),
('1FN9TT', 'Guest House Paradiso', 'SAS', 'Space Systems', 'Surveillance Systems', 1, 73166765418, 1),
('12PTMS', 'Dancing in September', 'SAS', 'Maritime', 'Sonar & Command Systems', 4, 32784039589, 1),
('1GYDR3', 'White Light/Black Rain: The Destruction of Hiroshima and Nagasaki', 'SAS', 'Space Systems', 'Surveillance Systems', 1, 39446257374, 1),
('1CEEPU', 'Dirties, The', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 60202819412, 1),
('184ET1', 'Firefox', 'SAS', 'Space Systems', 'Spectral Solutions', 3, 38585327304, 0),
('1QFMCE', 'Last Ride', 'SAS', 'Intelligence & Cyber', 'I&C International', 1, 21841125334, 1),
('1LJRDK', 'Airborne', 'SAS', 'Space Systems', 'Surveillance Systems', 2, 48633612551, 1),
('1TBUFR', 'Grifters, The', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 38405905142, 0);
GO