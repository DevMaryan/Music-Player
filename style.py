def groupboxStyle():
    return """
        QGroupBox {
        background-color: #252526;
        color:white;
        border-radius:3px;
        }
    """

def progressBarStyle():
    return """
        QProgressBar {
        height:5px;
        border: 1px solid #999;
        background: #333;
        border-radius:3px;
        }
    """

def LabelStyle():
    return """
        color:white;

    """

def playListStyle():
    return """
        QListWidget{
        padding:5px;
        background-color:#121212;
        border: 1px solid #212121;
        }
        QListWidget::item:selected{
        background-color:#252526;
        color:white;
        border:none;
        }

    """
def mainWindowBG():
    return """
        background-color:#252526;
        color:white;

    """

def playStyle():
    return """
        border: none;
        color:white;

    """

def sliderStyle():
    return """
        QSlider::groove:horizontal {
            border: 1px solid #999;
            height: 10px;
            margin: 0px;
            border-radius:5px;
            background-color:#333;
            }
        QSlider::handle:horizontal {
            background-color: #121212;
            color:white;
            height: 30px;
            width: 30px;
            margin: -15px 0px;
            border-radius:3px;
            }
    """