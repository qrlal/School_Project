using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class timer : MonoBehaviour
{
    private float time = 0;
    private Text text;
    // Start is called before the first frame update
    void Start()
    {
        text = this.gameObject.GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
        if (NoAnswer.start)
        {
            time += Time.deltaTime;
            text.text = string.Format("TIme : {0}", time);
            Debug.Log(time);
        }
    }
}
