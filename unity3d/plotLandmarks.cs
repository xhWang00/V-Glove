using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class LandmarkPlotter : MonoBehaviour
{
    public GameObject landmarkPrefab;
    public string apiUrl = "http://localhost:5000/landmarks";
    public float updateInterval = 0.1f;

    private void Start()
    {
        StartCoroutine(UpdateLandmarks());
    }

    IEnumerator UpdateLandmarks()
    {
        while (true)
        {
            UnityWebRequest www = UnityWebRequest.Get(apiUrl);
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError(www.error);
            }
            else
            {
                string jsonResponse = www.downloadHandler.text;
                LandmarkData[] landmarks = JsonHelper.FromJson<LandmarkData>(jsonResponse);
                
                Debug.Log(landmarks);

                // Delete existing landmarks
                GameObject[] existingLandmarks = GameObject.FindGameObjectsWithTag("Landmark");
                foreach (GameObject landmark in existingLandmarks)
                {
                    Destroy(landmark);
                }

                // Create new landmarks
                foreach (LandmarkData landmarkData in landmarks)
                {
                    Vector3 position = new Vector3(landmarkData.x, landmarkData.y, landmarkData.z);
                    Instantiate(landmarkPrefab, position, Quaternion.identity);
                }
            }

            yield return new WaitForSeconds(updateInterval);
        }
    }
}

[System.Serializable]
public class LandmarkData
{
    public float x;
    public float y;
    public float z;
}

public static class JsonHelper
{
    public static T[] FromJson<T>(string json)
    {
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
        return wrapper.Items;
    }

    [System.Serializable]
    private class Wrapper<T>
    {
        public T[] Items;
    }
}
