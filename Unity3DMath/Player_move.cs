using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player_move : MonoBehaviour
{
    public float speed = 1f;

    private float hAxis;
    private float vAxis;
    private float hAxisR;
    private float vAxisR;

    public static Vector3 movevec;
    public static Vector3 lookvec;

    void Update()
    {
        hAxis = Input.GetAxis("Horizontal");
        vAxis = Input.GetAxis("Vertical");

        hAxisR = Input.GetAxisRaw("Horizontal");
        vAxisR = Input.GetAxisRaw("Vertical");

        lookvec = new Vector3(hAxisR, 0, vAxisR).normalized;
        movevec = new Vector3(hAxis, 0, vAxis).normalized;

        //transform.LookAt(lookvec);
        transform.position += movevec * speed * Time.deltaTime;
    }
}
