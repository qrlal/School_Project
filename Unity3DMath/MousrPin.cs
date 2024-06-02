using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MousrPin : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.K))
        {
            Cursor.lockState = CursorLockMode.Locked;
        }

        if (Input.GetKeyUp(KeyCode.N))
        {
            Cursor.lockState = CursorLockMode.None;
        }
    }
}
