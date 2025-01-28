from langchain_core.tools import tool
import requests

base_url = "https://app-api-aka-mss-dev-003.azurewebsites.net"


# Define allowed medical record values
ALLOWED_MEDICAL_RECORDS = {
        "hypertension", "hypotension", "stroke", "dementia", "gout", "kidney_disease", "high_cholesterol", "diabetes", "cancer",
        "physical_disability", "operation_record", "vaccinated_past_year", "pain", "skin_disease"
}

@tool
def get_member_info(
    nameCh: str = None,
    ageFm: int = None,
    ageTo: int = None,
    sex: str = None,
    isDiabetes: bool = None,
    isHeartDisease: bool = None,
    isDementia: bool = None,
    MedicalRecord: str = None,
    topK: int = 10
    ) -> str:
    """
    Fetch the member information for a given Chinese name and specified criteria.

    Args:

        nameCh (str, optional): Chinese name of the member.
        ageFm (int, optional): Minimum age filter.
        ageTo (int, optional): Maximum age filter.
        sex (str, optional): Gender filter ("MEMBER_INFO_SEX|male", "MEMBER_INFO_SEX|female").
        isDiabetes (bool, optional): Filter by diabetes status.
        isHeartDisease (bool, optional): Filter by heart disease status.
        isDementia (bool, optional): Filter by dementia status.
        MedicalRecord (str, optional): Filter by a specific medical record. Must be one of the predefined allowed values from below.
        topK (int, optional): Max number of results to return.

    MedicalRecord List:
        "hypertension", "hypotension", "stroke", "dementia", "gout", "kidney_disease", "high_cholesterol", "diabetes", "cancer",
        "physical_disability", "pain", "skin_disease"

    Returns:
        str: A JSON-formatted string containing the searched member information or an error message.
    """
    api_url = f"{base_url}/api/Tester/GetMemberInfo"

    if MedicalRecord and MedicalRecord not in ALLOWED_MEDICAL_RECORDS:
      return f"Invalid MedicalRecord value. Allowed values are: {', '.join(ALLOWED_MEDICAL_RECORDS)}"


    try:
        # Prepare query parameters, excluding any that are None
        params = {
            "nameCh": nameCh,
            "ageFm": ageFm,
            "ageTo": ageTo,
            "sex": sex,
            "isDiabetes": isDiabetes,
            "isHeartDisease": isHeartDisease,
            "isDementia": isDementia,
            "MedicalRecord": MedicalRecord,
            "topK": topK,
        }
        # Remove keys with None values
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the API: {e}"
    except KeyError:
        return "Unexpected response structure from the API."

@tool
def get_member_icp(memberTeamSysId: int) -> str:
  """
  Fetch the member individual care plan full list for a given member team sysId

  Args:
      memberTeamSysId (int): The system id of that is uniquely identifying the member

  Returns:
      str: A json format of the member's individual care plan.
  """
  api_url = f"{base_url}/api/Tester/GetMemberInfoICP"

  try:
        response = requests.get(api_url, params={"memberTeamSysId": memberTeamSysId})
        response.raise_for_status()
        data = response.json()
        return data
  except requests.exceptions.RequestException as e:
      return f"An error occurred while fetching the api: {e}"
  except KeyError:
      return "Unexpected response structure from the API."