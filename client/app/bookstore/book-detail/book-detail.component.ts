import { ActivatedRoute, Router } from '@angular/router';
import { Http } from '@angular/http';
import { Book } from './../model/book';
import { BookService } from './../book.service';
import { Component, OnInit } from '@angular/core';
import { saveAs } from 'file-saver';
import { ResponseContentType } from '@angular/http';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-book-detail',
  templateUrl: './book-detail.component.html',
  styleUrls: ['./book-detail.component.scss']
})
export class BookDetailComponent implements OnInit {
  bookDetail: Book = new Book();
  bookID: string;

  constructor(
    private _activatedRoute: ActivatedRoute,
    private _bookService: BookService,
    private _http: Http,
    private _snackBarService: MatSnackBar,
    private _router: Router,
  ) { }

  ngOnInit() {
    this._activatedRoute.params.subscribe(
      params => {
        this.getBookDetail(params['bookID']);
        this.bookID = params['bookID'];
      }
    );
  }

  private getBookDetail(bookID: string) {
    this._bookService
      .getBookDetail(bookID)
      .subscribe(data => {
        console.log('book detail: ', data.json().result)
        this.bookDetail = data.json().result;
      },
      (error) => {
        console.log("error???", error.json());
        if (error.json().errors[0].code === "book_not_exist") {
          this._snackBarService.open("The book does not exist", 'Error', {
            duration: 5000,
          })
        }
        this._bookService.deleteABook(bookID).toPromise();
        // TODO: back to where you come from
        this._router.navigate(['/bookstore']);
      }
    );
  }

  private downloadFile() {
    console.log('Download file');
    console.log('download url: ', this.bookDetail.download_url);
    // this._http.get('http://localhost:19000/books/ee-bookorg-%E9%98%AE%E4%B8%80%E5%B3%B0%E7%9A%84%E7%BD%91%E7%BB%9C%E6%97%A5%E5%BF%97-rss-2017-10-01.epub?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=DFEEHK4IPJQAXDW8M7A9%2F20171005%2F%2Fs3%2Faws4_request&X-Amz-Date=20171005T063745Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=6e6df38027073f488befa21abd077791bf996ce5a5787610b7b69f46234958aa', {responseType: ResponseContentType.Blob}).subscribe(
    this._http.get(this.bookDetail.download_url,
      {responseType: ResponseContentType.Blob}).subscribe(
        (response) => {
          const mediaType = 'application/epub+zip';
          const blob = new Blob([response.blob()], {type: mediaType});
          const filename = this.bookDetail.title;
          saveAs(blob, filename);
        });
  }

  private goBack() {
    this._router.navigate(['/']);
  }
}
