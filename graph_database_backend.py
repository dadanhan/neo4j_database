from pathlib import Path
import dotenv
import os
import neo4j as nj

#load hidden file for environment variables containing sensitive information
env_path = Path.cwd() / ".neo4j_credentials"
load_status = dotenv.load_dotenv(env_path)
if not load_status:
    raise RuntimeError('Environment variables not loaded.')

#from environment variables get URI, username and password to connect to neo4j database
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

#function to add patient to database
def addValue(tx,label,field,val):
    query = f"""
        MERGE (p:{label} {{{field}: $val}})
        RETURN p.{field} AS field_value
    """
    result = tx.run(query, val=val)
    record = result.single()
    if record:
        return label, field, record["field_value"]
    else:
        return label, field, None  # In case something goes wrong
    
# Function to read all values from the database in a field
def readValues(tx, label, field):
    query = f"""
        MATCH (p:{label})
        RETURN p.{field} AS field_value
    """
    result = tx.run(query)
    return [record.get("field_value") for record in result if record.get("field_value")]

if __name__ == "__main__":
    #read in file containing all the fields we want to associate with each patient
    fields = Path(".patient_fields").read_text().splitlines()
    print('Fields for person entry:',fields)

    with nj.GraphDatabase.driver(URI, auth=AUTH) as driver: #connect to database
        driver.verify_connectivity()
        print("Connection to database established")
        with driver.session(database="neo4j") as session: #open session
            #create person
            lbl,fld,val = session.execute_write(addValue, label="Person", field=fields[0], val="ALICE")
            print(f"{fld} {val} added to {lbl}")

            #read values from database
            all_values = session.execute_read(readValues, label=lbl, field=fld)
            print(f"All {fld}s in {lbl}: {all_values}")