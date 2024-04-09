using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class LandmarkPlotter : MonoBehaviour
{
    public GameObject landmarkPrefab;
    public string apiUrl = "http://localhost:5000/landmarks";
    public float updateInterval = 0.01f;

    private void Start()
    {
        StartCoroutine(UpdateLandmarks());
    }

    private void connect_landmarks(GameObject[] objs, int start, int end)
    {
        var obj = new GameObject();
        obj.tag = "Line";

        var lineRender = obj.AddComponent<LineRenderer>();
        lineRender.startWidth = 0.03f;
        lineRender.endWidth = 0.03f;
        lineRender.material.color = Color.white;

        GameObject start_obj = objs[start];
        GameObject end_obj = objs[end];

        lineRender.SetPosition(0, start_obj.transform.position);
        lineRender.SetPosition(1, end_obj.transform.position);
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

                // Delete existing landmarks
                GameObject[] existingLandmarks = GameObject.FindGameObjectsWithTag("Landmark");
                foreach (GameObject landmark in existingLandmarks)
                {
                    Destroy(landmark);
                }
                int i = 0;
                GameObject[] objArr = new GameObject[21];
                GameObject[] existingLines = GameObject.FindGameObjectsWithTag("Line");
                foreach (GameObject line in existingLines)
                {
                    Destroy(line);
                }

                // Create new landmarks
                foreach (LandmarkData landmarkData in landmarks)
                {
                    Vector3 position = new Vector3(landmarkData.x, landmarkData.y, landmarkData.z);

                    GameObject obj = Instantiate(landmarkPrefab, position, Quaternion.identity);
                    objArr[i] = obj;
                    i++;
                }

                connect_landmarks(objArr, 0, 17);
                connect_landmarks(objArr, 0, 1);
                connect_landmarks(objArr, 1, 2);
                connect_landmarks(objArr, 2, 5);
                connect_landmarks(objArr, 5, 9);
                connect_landmarks(objArr, 9, 13);
                connect_landmarks(objArr, 13, 17);

                connect_landmarks(objArr, 2, 3);
                connect_landmarks(objArr, 3, 4);

                connect_landmarks(objArr, 5, 6);
                connect_landmarks(objArr, 6, 7);
                connect_landmarks(objArr, 7, 8);

                connect_landmarks(objArr, 9, 10);
                connect_landmarks(objArr, 10, 11);
                connect_landmarks(objArr, 11, 12);

                connect_landmarks(objArr, 13, 14);
                connect_landmarks(objArr, 14, 15);
                connect_landmarks(objArr, 15, 16);

                connect_landmarks(objArr, 17, 18);
                connect_landmarks(objArr, 18, 19);
                connect_landmarks(objArr, 19, 20);
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
