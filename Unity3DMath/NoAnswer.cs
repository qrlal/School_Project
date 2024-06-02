using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NoAnswer : MonoBehaviour
{
    public static bool start = false;

    //float time = 0;
    float dis = 0;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetMouseButtonDown(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;
            if(Physics.Raycast(ray, out hit))
            {
                dis = hit.distance;

                Debug.Log(dis);
                if(hit.transform.gameObject.tag == "no" && dis < 4)
                {
                    transform.position = new Vector3(0, 2, 0);
                    Move.speed = Move.speed * 0.8f;
                }

                if (hit.transform.gameObject.tag == "golv1" && dis < 4)
                {
                    transform.position = new Vector3(0, 2, 20);
                    start = true;
                }

                if (hit.transform.gameObject.tag == "golv3" && dis < 4)
                {
                    transform.position = new Vector3(6, 2, 92);
                }

                if (hit.transform.gameObject.tag == "golv2" && dis < 4)
                {
                    transform.position = new Vector3(0, 2, 48);
                }
            }
        }
    }
}
