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
    contract_type VARCHAR(1028) NOT NULL,
    contract_number VARCHAR(1028) NOT NULL,
    contract_value BIGINT NOT NULL,
    contract_start_date DATE,
    contract_end_date DATE,
    actual_cost_work_performed_cumulative FLOAT,
    budgeted_cost_work_performed_cumulative FLOAT,
    budgeted_cost_work_scheduled_cumulative FLOAT,
    cost_performance_index_cumulative FLOAT,
    schedule_performance_index_cumulative FLOAT,
    budget_at_complete FLOAT,
    estimate_at_complete FLOAT,
    estimate_to_complete FLOAT,
    management_reserve FLOAT,
    weighted_risks_and_opportunities FLOAT,
    active_status BIT NOT NULL,
    PRIMARY KEY (id)
);
GO

INSERT INTO [program] (pa_number, program_name, segment, sector, division, tier, contract_type, contract_number, contract_value, contract_start_date, contract_end_date, actual_cost_work_performed_cumulative, budgeted_cost_work_performed_cumulative, budgeted_cost_work_scheduled_cumulative, cost_performance_index_cumulative, schedule_performance_index_cumulative, budget_at_complete, estimate_at_complete, estimate_to_complete, management_reserve, weighted_risks_and_opportunities, active_status)
VALUES 
('1PHLMV', 'Quo Vadis', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 2, 'FFP', 'CN010193', 31415629467, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1DVH8T', 'Painted Lady', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 'FFP', 'CN010194', 83233449721, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1FAGGW', 'Why Has Bodhi-Dharma Left for the East?: A Zen Fable', 'SAS', 'Space Systems', 'Surveillance Systems', 2, 'FFP', 'CN010195', 36353475629, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('19MSTR', 'Emperor Waltz, The', 'SAS', 'Space Systems', 'Surveillance Systems', 2, 'FFP', 'CN010196', 89919689752, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1K6BHP', 'Innocent Blood', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 'FFP', 'CN010197', 15086029062, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1LF37L', 'House of Angels', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 2, 'FFP', 'CN010198', 17058313872, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1DUMVC', 'Red Dawn', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 'FFP', 'CN010197', 58931283490, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('19OXB6', 'Snow Dogs', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 'FFP', 'CN010180', 13866035610, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1H3EZJ', 'Boys on the Side', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 3, 'FFP', 'CN010280', 68219679290, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1QJYDE', 'Boogeyman', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 'FFP', 'CN010380', 16509455949, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1AOXVN', 'So Proudly We Hail!', 'SAS', 'Space Systems', 'Spectral Solutions', 4, 'FFP', 'CN010381', 8112327131, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1GLKRQ', 'That Darn Cat!', 'SAS', 'Space Systems', 'Spectral Solutions', 1, 'FFP', 'CN010382', 38652687145, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1BSDOZ', 'Puss in Boots', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 'FFP', 'CN010383', 3252030265, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1NQMHN', 'High Cost of Living, The', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 'FFP', 'CN010384', 33625325875, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('1M2NX2', 'Lilo & Stitch', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 'FFP', 'CN010385', 20481866256, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('171UBT', 'Rammbock', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 'FFP', 'CN010375', 81027154087, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('1KBUTC', 'Journey to the West: Conquering the Demons', 'SAS', 'Intelligence & Cyber', 'I&C International', 4, 'FFP', 'CN010376', 81055210605, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('12GMTV', "Li'l Abner", 'SAS', 'Intelligence & Cyber', 'I&C International', 1, 'FFP', 'CN010377', 90852477864, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('16NQZX', 'Piece of the Action, A', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 1, 'FFP', 'CN010378', 45323906089, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1KVLSH', "Emperor's Naked Army Marches On, The", 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 2, 'FFP', 'CN010379', 10726575487, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('1FGEDU', 'Terror, The', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 'FFP', 'CN010401', 33812880158, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1NJEHC', 'Corto Maltese: Ballad of the Salt Sea', 'SAS', 'Intelligence & Cyber', 'I&C International', 2, 'FFP', 'CN010402', 2030023640, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('16NEWS', 'Pleasure Party', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 'FFP', 'CN010403', 86957852141, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1EBGMK', 'Middle of Nowhere', 'SAS', 'Intelligence & Cyber', 'Tactical Missions', 3, 'FFP', 'CN010404', 88668842695, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('1H6YX2', 'Scream 4', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 'FFP', 'CN010405', 10725446581, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('198W8H', "Rally 'Round the Flag, Boys!", 'SAS', 'Intelligence & Cyber', 'I&C International', 1, 'FFP', 'CN010406', 16975340832, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('17VYPD', 'Bend of the River', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 'FFP', 'CN010407', 12535401324, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1FB8JE', 'Quick and the Dead, The', 'SAS', 'Maritime', 'Sonar & Command Systems', 2, 'FFP', 'CN010408', 14087001047, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('197DTK', 'New World, The', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 'FFP', 'CN010409', 10379047809, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1MYYSX', 'Junebug', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 3, 'FFP', 'CN010509', 11400812145, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1M1BCG', 'Land of the Pharaohs', 'SAS', 'Airborne Combat Systems', 'Military Avionics', 4, 'FFP', 'CN005009', 12346314307, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('16BS1F', 'The Conrad Boys', 'SAS', 'Maritime', 'Sonar & Command Systems', 4, 'FFP', 'CN030009', 16490706138, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1FN9TT', 'Guest House Paradiso', 'SAS', 'Space Systems', 'Surveillance Systems', 1, 'FFP', 'CN030019', 73166765418, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('12PTMS', 'Dancing in September', 'SAS', 'Maritime', 'Sonar & Command Systems', 4, 'FFP', 'CN030119', 32784039589, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1GYDR3', 'White Light/Black Rain: The Destruction of Hiroshima and Nagasaki', 'SAS', 'Space Systems', 'Surveillance Systems', 1, 'FFP', 'CN030129', 39446257374, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1CEEPU', 'Dirties, The', 'SAS', 'Airborne Combat Systems', 'Electronic Warfare', 2, 'FFP', 'CN031129', 60202819412, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('184ET1', 'Firefox', 'SAS', 'Space Systems', 'Spectral Solutions', 3, 'FFP', 'CN031329', 38585327304, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0),
('1QFMCE', 'Last Ride', 'SAS', 'Intelligence & Cyber', 'I&C International', 1, 'FFP', 'CN031829', 21841125334, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1LJRDK', 'Airborne', 'SAS', 'Space Systems', 'Surveillance Systems', 2, 'FFP', 'CN031729', 48633612551, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1),
('1TBUFR', 'Grifters, The', 'SAS', 'Maritime', 'Sonar & Command Systems', 3, 'FFP', 'CN032729', 38405905142, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0);
GO