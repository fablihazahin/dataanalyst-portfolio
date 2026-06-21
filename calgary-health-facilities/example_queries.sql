-- How many facilities of each type
  SELECT t.type, COUNT(*) AS n
  FROM facility f JOIN type_lookup t ON f.type_id = t.type_id
  GROUP BY t.type ORDER BY n DESC;

  -- Facilities in a given community (community code 'CAP')
  SELECT f.name, f.address
  FROM facility f JOIN community_lookup c ON f.comm_code_id = c.comm_code_id
  WHERE c.comm_code = 'CAP';

  -- Data-quality check: facilities missing an address
  SELECT name FROM facility WHERE address IS NULL;