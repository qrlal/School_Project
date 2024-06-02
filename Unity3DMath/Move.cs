using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using UnityEngine;

public class Move : MonoBehaviour
{
    private Rigidbody rb;
    public Camera TheCamera;
    float timer = 0;

    public static float speed = 3;
    public float jump_P;
    public float jump_deley;

    //private bool isGround;

    private float hA;
    private float vA;
    private Vector3 movevec;

    public float looksen;
    public float cameralimit;
    private float currentcameraX = 0f;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();    
    }

    // Update is called once per frame
    void Update()
    {
        hA = Input.GetAxisRaw("Horizontal");
        vA = Input.GetAxisRaw("Vertical");
        movevec = (transform.right * hA + transform.forward * vA).normalized * speed;

        //rb.MovePosition(transform.position + movevec * Time.deltaTime);
        transform.position += movevec * speed * Time.deltaTime;

        timer += Time.deltaTime;
        if (Input.GetButton("Jump") && timer >1.05)
        {
            rb.AddForce(Vector3.up * jump_P, ForceMode.Impulse);
            timer = 0;
            //isGround = false;
        }

        CameraRot();
        CharacterRot();
    }

    private void CameraRot()
    {
        float Xrot = Input.GetAxisRaw("Mouse Y");
        float CameraRotX = -Xrot * looksen;

        currentcameraX += CameraRotX;
        currentcameraX = Mathf.Clamp(currentcameraX, -cameralimit, cameralimit);

        TheCamera.transform.localEulerAngles = new Vector3(currentcameraX, 0f, 0f);
    }

    private void CharacterRot()
    {
        float Yrot = Input.GetAxisRaw("Mouse X");
        Vector3 characterrotY =new Vector3(0f, Yrot, 0f) * looksen;
        rb.MoveRotation(rb.rotation * Quaternion.Euler(characterrotY));
    }

    //void OnCollisionEnter(Collision collision)
    //{
        // 부딪힌 물체의 태그가 "Ground"라면
    //    if (collision.gameObject.CompareTag("Ground"))
    //    {
    //        // isGround를 true로 변경
    //        isGround = true;
    //    }
    //}
}
