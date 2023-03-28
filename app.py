from flask import Flask, render_template, request
import yt_web_scraping, yt_sentimental_analysis , delete_files_image


app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yt_comments_sa.db'
# db= SQLAlchemy(app)
#
# class Comment_SA(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     comment = db.Column(db.String(500),nullable=False)

# def __repr__(self):
#     return
@app.route("/")
def home():
    return render_template('yt_sentiment_analysis.html')

@app.route('/scrap',methods=['GET','POST'])
def index():
    # url = 'https://www.youtube.com/watch?v=KfiTET8RJ9A'
    url = request.form.get('youtube url')
    yt_comments_details = yt_web_scraping.yt_scrapper(url)
    pos, neg, neu = yt_sentimental_analysis.sentiment_analyser('Youtube_comments.csv')
    video_title, video_owner, views, total_comments = yt_comments_details[1:]
    complete_message = 'All details of video extracted'
    delete_files_image.delete()
    return render_template('yt_sentiment_analysis.html', complete_message=complete_message, title=video_title, owner=video_owner,
                           views=views, total_comments=total_comments,
                           positive_comments=[pos.to_html(classes='data', header="true")],
                           negative_comments=[neg.to_html(classes='data', header="true")],
                           neutral_comments= [neu.to_html(classes='data', header="true")])


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0',debug=True)
